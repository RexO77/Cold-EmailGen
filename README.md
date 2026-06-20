# Cold Email Generator 📧

**Cold-EmailGen** turns your résumé and a job-posting URL into a cold email grounded
in your *actual* experience — plus an honest read on whether you're even a fit for the
role. Upload a résumé, paste a job link, and it scrapes the posting, matches it against
your background, and drafts the email. No templates, no invented credentials.

## Features 🔑
- **Résumé-driven** — upload a PDF, DOCX, or TXT. It's parsed and embedded into a local
  vector store (ChromaDB); no CSV or manual data entry.
- **Honest fit assessment** — for each role it returns a verdict (*Strong fit / Possible
  fit / Stretch / Not a fit*), where you match, where you fall short, and how to improve.
- **Grounded emails** — every claim is drawn from your résumé; it won't fabricate
  employers, skills, or metrics.
- **Job-posting scraping** — reads the careers/job URL with LangChain's `WebBaseLoader`.
- **Polished Streamlit UI** — dark, glassy interface with a dedicated results page.

## Quick start ⚙️

```bash
git clone https://github.com/RexO77/Cold-EmailGen.git
cd Cold-EmailGen
./run.sh
```

`run.sh` sets everything up on first run (creates a virtualenv, installs dependencies)
and starts the server; on later runs it goes straight to launching the app. Then open
**http://localhost:8501**.

> Run on a different port with `PORT=8600 ./run.sh`.

### API key
The app uses **Groq** for inference. On first run it creates `App/.env` from
`App/.env.example` — add your key:

```
GROQ_API_KEY=your_groq_api_key
```

Get one at https://console.groq.com/keys. (`.env` is gitignored — never commit it.)

### Manual setup (alternative to run.sh)
Requires **Python 3.11–3.13** (3.14+ can't build the pinned dependencies).

```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp App/.env.example App/.env   # then add your GROQ_API_KEY
streamlit run App/main.py
```

## How it works ⚙️
1. **Ingest** — your résumé is parsed (`App/resume_parser.py`), chunked, and embedded into
   ChromaDB (`App/store.py`). A new upload replaces the previous résumé.
2. **Scrape & extract** — the job URL is fetched and cleaned, then an LLM extracts the
   postings as structured JSON (role, experience, skills, description).
3. **Assess & write** — for each role, a single LLM call judges fit against your full
   résumé and drafts the email (`App/chains.py`).
4. **Present** — results render on their own page with a color-coded fit card above each
   draft (`App/main.py`, `App/styles.py`).

## Tech stack 🛠️
- **Streamlit** — web front-end
- **LangChain + Groq** (`llama-3.1-8b-instant`) — extraction, assessment, and email drafting
- **ChromaDB** — local vector store for the résumé
- **pypdf / python-docx** — résumé parsing

## Contributing 🤝
Contributions welcome — open an issue or a pull request.
