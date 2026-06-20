import html

import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from store import ResumeStore
from resume_parser import extract_resume_text, content_hash, SUPPORTED_TYPES
from styles import CSS, HERO
from utils import clean_text

MAX_ROLES = 5  # cap roles per run — keeps output focused and within rate limits

VERDICT_CLASS = {
    "Strong fit": "v-strong",
    "Possible fit": "v-possible",
    "Stretch": "v-stretch",
    "Not a fit": "v-no",
}


def esc(s):
    return html.escape(str(s))


def fit_card_html(a):
    """Build the honest fit-assessment card from an assess_and_write result."""
    verdict = a.get("verdict", "Possible fit")
    cls = VERDICT_CLASS.get(verdict, "v-possible")

    def section(title, items, ul_class, icon):
        items = [i for i in (items or []) if str(i).strip()]
        if not items:
            return ""
        lis = "".join(f'<li><span class="ic">{icon}</span>{esc(i)}</li>' for i in items)
        return f'<div class="fit-sec"><h4>{title}</h4><ul class="{ul_class}">{lis}</ul></div>'

    body = section("Why you fit", a.get("strengths"), "strengths", "✓")
    body += section("Gaps", a.get("gaps"), "gaps", "!")
    body += section("How to close them", a.get("improve"), "improve", "→")

    summary = esc(a.get("summary", ""))
    return (
        f'<div class="fit-card"><span class="verdict {cls}">{esc(verdict)}</span>'
        f'<p class="fit-summary">{summary}</p>{body}</div>'
    )


def render_form(store):
    """Page 1 — résumé + job link."""
    st.markdown(HERO, unsafe_allow_html=True)

    # ── Step 1 — Résumé ──────────────────────────────────────────────────
    with st.container(border=True):
        st.markdown('<div class="step">Step <b>1</b></div>', unsafe_allow_html=True)
        st.markdown("##### Your résumé")
        resume_file = st.file_uploader(
            "résumé upload", type=SUPPORTED_TYPES, label_visibility="collapsed",
            help="PDF, DOCX, or TXT. Stays on your machine.",
        )

        if resume_file is not None:
            file_id = content_hash(resume_file)
            if st.session_state.get("resume_id") != file_id:
                with st.spinner("Reading your résumé…"):
                    try:
                        text = extract_resume_text(resume_file)
                        n = store.ingest(text, file_id)
                        st.session_state.update(resume_id=file_id, resume_chunks=n)
                    except Exception as e:
                        st.session_state.pop("resume_id", None)
                        st.error(f"Couldn't read that file. {e}")

        if store.has_resume() and st.session_state.get("resume_id"):
            st.markdown(
                f'<div class="ready"><span class="check">✓</span> '
                f"Résumé ready &middot; <b>{st.session_state.get('resume_chunks', 0)}</b> "
                f"passages indexed</div>",
                unsafe_allow_html=True,
            )

    # ── Step 2 — Job posting ─────────────────────────────────────────────
    with st.container(border=True):
        st.markdown('<div class="step">Step <b>2</b></div>', unsafe_allow_html=True)
        st.markdown("##### The job you're after")
        url_input = st.text_input(
            "job url", value=st.session_state.get("job_url", ""),
            label_visibility="collapsed",
            placeholder="Paste a job-posting or careers-page URL",
        )
        submit = st.button("Write my email  →", type="primary")

    if submit:
        if not store.has_resume():
            st.warning("Add your résumé first — it's what the email is built from.")
            return
        if not url_input.strip():
            st.warning("Add a job link — that's what the email responds to.")
            return
        # Hand off to the results page.
        st.session_state.job_url = url_input.strip()
        st.session_state.view = "results"
        st.session_state.pop("results", None)
        st.rerun()


def friendly_error(e):
    """Turn raw exceptions into calm, blameless guidance."""
    msg = str(e).lower()
    if "rate_limit" in msg or "429" in msg or "tokens per minute" in msg:
        return "Hit the model's rate limit for this minute. Wait ~30 seconds and try again."
    if "api_key" in msg or "401" in msg or "invalid api key" in msg:
        return "The Groq API key looks invalid. Check the key in App/.env and try again."
    return "Something went wrong generating the email. Try again in a moment."


def generate(llm, store, url):
    """Scrape → extract jobs → write one email per role. Returns (drafts, error)."""
    try:
        loader = WebBaseLoader([url])
        data = clean_text(loader.load().pop().page_content)
    except Exception:
        return None, "Couldn't load that page. Check the URL and try again."

    try:
        jobs = llm.extract_jobs(data)
    except Exception as e:
        return None, friendly_error(e)

    if not jobs:
        return [], None, 0

    total = len(jobs)
    resume_text = store.full_text()
    drafts = []
    for job in jobs[:MAX_ROLES]:
        role = job.get("role", "this role")
        try:
            result = llm.assess_and_write(job, resume_text)
        except Exception as e:
            return None, friendly_error(e), total
        result["role"] = role
        drafts.append(result)
    return drafts, None, total


def render_results(llm, store):
    """Page 2 — the generated drafts, on their own screen."""
    if st.button("←  Start over", type="secondary"):
        st.session_state.view = "form"
        st.rerun()

    url = st.session_state.get("job_url", "")

    if "results" not in st.session_state:
        with st.spinner("Reading the posting and matching it to your résumé…"):
            st.session_state.results = generate(llm, store, url)
    drafts, error, total = st.session_state.results

    if error:
        st.error(error)
        return
    if not drafts:
        st.info("No job posting found on that page. Try the direct posting URL.")
        return

    n = len(drafts)
    note = f" &middot; {total} roles found on the page, assessing the first {n}" if total > n else ""
    st.markdown(
        f'<div class="page-head"><h2>{n} role{"s" if n > 1 else ""} assessed</h2>'
        f'<p>An honest read on each fit — then a draft you can send.{note}</p></div>',
        unsafe_allow_html=True,
    )
    for d in drafts:
        st.markdown(
            f'<div class="result-head">{esc(d.get("role", "this role"))}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(fit_card_html(d), unsafe_allow_html=True)
        st.markdown('<div class="draft-label">Suggested cold email</div>', unsafe_allow_html=True)
        st.code(d.get("email", ""), language="markdown")


def main():
    st.set_page_config(page_title="Cold Mail Generator", page_icon="📧", layout="centered")
    st.markdown(CSS, unsafe_allow_html=True)

    chain = Chain()
    store = ResumeStore()

    if st.session_state.get("view") == "results":
        render_results(chain, store)
    else:
        render_form(store)


if __name__ == "__main__":
    main()
