"""Dark, glassy design system for the Cold Mail Generator.

All visual styling lives here as injected CSS so main.py stays about flow, not
appearance. Motion uses CSS keyframes with spring-like easing (the closest a
Streamlit app gets to Framer Motion). Timing constants are named at the top so
they read like a storyboard.
"""

# ── Storyboard ────────────────────────────────────────────────────────────────
#    0ms   page backdrop gradient drifts (22s loop, ambient)
#    0ms   each main block fades up + settles (staggered 60ms)
#  hover   primary button lifts 2px and blooms its glow (180ms)
# ────────────────────────────────────────────────────────────────────────────

ACCENT = "#8B743D"          # gold — brand / primary action / focus
ACCENT_BRIGHT = "#A8894A"   # brighter gold — gradient start
ACCENT_DEEP = "#6E5B30"     # deeper gold — gradient end
ACCENT_2 = "#C7A867"        # champagne — gradient highlight
BASE = "#12162D"            # navy — page base
EASE = "cubic-bezier(0.22, 1, 0.36, 1)"   # spring-like overshoot-free ease-out

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {{
  --accent: {ACCENT};
  --accent-bright: {ACCENT_BRIGHT};
  --accent-deep: {ACCENT_DEEP};
  --accent-2: {ACCENT_2};
  --glass-bg: rgba(255, 255, 255, 0.04);
  --glass-border: rgba(255, 255, 255, 0.10);
  --text: #ECEDF2;
  --muted: #9aa0b8;
  --ok: #34d399;
  --ease: {EASE};
}}

/* ── Typography ─────────────────────────────────────────────────────────── */
html, body, [class*="st-"], .stMarkdown, input, button, textarea {{
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}}
/* Keep Streamlit's material icons as glyphs — never reflow them to Inter */
[data-testid="stIconMaterial"], .material-icons, [class*="material-symbols"] {{
  font-family: 'Material Symbols Rounded' !important;
}}

/* ── Animated ambient backdrop ─────────────────────────────────────────── */
.stApp {{
  background:
    radial-gradient(60rem 60rem at 12% -10%, rgba(139, 116, 61, 0.18), transparent 60%),
    radial-gradient(55rem 55rem at 100% 0%, rgba(199, 168, 103, 0.09), transparent 55%),
    radial-gradient(50rem 50rem at 50% 120%, rgba(139, 116, 61, 0.12), transparent 60%),
    {BASE};
  background-attachment: fixed;
  animation: bgDrift 22s ease-in-out infinite alternate;
}}
@keyframes bgDrift {{
  0%   {{ background-position: 0% 0%, 100% 0%, 50% 100%; }}
  100% {{ background-position: 6% 4%, 94% 3%, 46% 96%; }}
}}

/* Transparent Streamlit chrome for a cleaner canvas */
[data-testid="stHeader"] {{ background: transparent; }}
[data-testid="stToolbar"] {{ right: 1rem; }}
#MainMenu, footer {{ visibility: hidden; }}

/* ── Layout ────────────────────────────────────────────────────────────── */
.block-container {{
  max-width: 760px;
  padding-top: 2.5rem;
  padding-bottom: 5rem;
}}

/* Entrance: fade up + settle, lightly staggered across top-level blocks */
.block-container > div > div > div > [data-testid="stVerticalBlock"] > div {{
  animation: fadeUp 0.6s var(--ease) both;
}}
.block-container > div > div > div > [data-testid="stVerticalBlock"] > div:nth-child(2) {{ animation-delay: 0.06s; }}
.block-container > div > div > div > [data-testid="stVerticalBlock"] > div:nth-child(3) {{ animation-delay: 0.12s; }}
.block-container > div > div > div > [data-testid="stVerticalBlock"] > div:nth-child(4) {{ animation-delay: 0.18s; }}
@keyframes fadeUp {{
  from {{ opacity: 0; transform: translateY(14px); }}
  to   {{ opacity: 1; transform: translateY(0); }}
}}

/* ── Hero ──────────────────────────────────────────────────────────────── */
.hero {{ margin: 0 0 2.2rem; }}
.hero h1 {{
  font-size: clamp(2.2rem, 5vw, 3.1rem); font-weight: 800; line-height: 1.05;
  letter-spacing: -0.03em; margin: 0 0 .6rem;
  background: linear-gradient(120deg, #ffffff 26%, var(--accent-2) 60%, var(--accent));
  -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
}}
.hero p {{ font-size: 1.06rem; color: var(--muted); max-width: 48ch; line-height: 1.55; }}

/* Results-page header */
.page-head {{ margin: .2rem 0 1.4rem; }}
.page-head h2 {{
  font-size: 1.7rem; font-weight: 800; letter-spacing: -0.02em; margin: 0 0 .3rem; color: var(--text);
}}
.page-head p {{ color: var(--muted); font-size: .98rem; }}

/* ── Glass cards (bordered containers) ─────────────────────────────────── */
[data-testid="stVerticalBlockBorderWrapper"] {{
  background: var(--glass-bg);
  border: 1px solid var(--glass-border) !important;
  border-radius: 20px !important;
  backdrop-filter: blur(18px) saturate(140%);
  -webkit-backdrop-filter: blur(18px) saturate(140%);
  box-shadow: 0 18px 50px -20px rgba(0,0,0,0.7), inset 0 1px 0 rgba(255,255,255,0.05);
  padding: .4rem .35rem;
  transition: border-color .3s var(--ease), box-shadow .3s var(--ease);
}}
[data-testid="stVerticalBlockBorderWrapper"]:hover {{
  border-color: rgba(139,116,61,0.42) !important;
}}

/* Step label */
.step {{ font-size: .8rem; font-weight: 600; letter-spacing: .02em; color: var(--muted); margin-bottom: .15rem; }}
.step b {{ color: var(--accent-2); }}

/* ── Buttons ───────────────────────────────────────────────────────────── */
.stButton > button {{
  font-weight: 600; font-size: .98rem;
  border: 0; border-radius: 13px; padding: .72rem 1.15rem;
  transition: transform .18s var(--ease), box-shadow .18s var(--ease),
              filter .18s var(--ease), border-color .18s var(--ease);
}}
/* Primary — gold gradient, dark navy text for crisp contrast, full width */
.stButton > button[kind="primary"] {{
  width: 100%; color: #14120A; font-weight: 700;
  background: linear-gradient(135deg, var(--accent-bright), var(--accent-deep));
  box-shadow: 0 8px 26px -8px rgba(139,116,61,0.75);
}}
.stButton > button[kind="primary"]:hover {{
  transform: translateY(-2px);
  box-shadow: 0 14px 34px -8px rgba(139,116,61,0.95);
  filter: brightness(1.08);
}}
.stButton > button[kind="primary"]:active {{ transform: translateY(0); }}
/* Secondary — ghost, auto width (back / start over) */
.stButton > button[kind="secondary"] {{
  background: rgba(255,255,255,0.04);
  border: 1px solid var(--glass-border);
  color: var(--text);
  box-shadow: none;
}}
.stButton > button[kind="secondary"]:hover {{
  border-color: var(--accent); transform: translateY(-1px);
}}

/* ── Text input ────────────────────────────────────────────────────────── */
[data-testid="stTextInput"] input {{
  background: rgba(255,255,255,0.04) !important;
  border: 1px solid var(--glass-border) !important;
  border-radius: 12px !important; color: var(--text) !important;
  padding: .65rem .85rem !important;
  transition: border-color .2s var(--ease), box-shadow .2s var(--ease);
}}
[data-testid="stTextInput"] input:focus {{
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 3px rgba(139,116,61,0.25) !important;
}}

/* ── File uploader dropzone ────────────────────────────────────────────── */
[data-testid="stFileUploaderDropzone"] {{
  background: rgba(255,255,255,0.03);
  border: 1.5px dashed rgba(139,116,61,0.45);
  border-radius: 14px;
  transition: border-color .2s var(--ease), background .2s var(--ease);
}}
[data-testid="stFileUploaderDropzone"]:hover {{
  border-color: var(--accent);
  background: rgba(139,116,61,0.07);
}}

/* ── Résumé "ready" line (borderless — no nested box) ──────────────────── */
.ready {{
  display: flex; align-items: center; gap: .5rem;
  margin: .65rem .15rem .15rem; font-size: .9rem; color: var(--muted);
}}
.ready .check {{
  color: var(--ok); font-weight: 800;
  text-shadow: 0 0 10px rgba(52,211,153,0.5);
}}
.ready b {{ color: var(--text); font-weight: 600; }}

/* ── Fit assessment card ───────────────────────────────────────────────── */
.fit-card {{
  background: rgba(255,255,255,0.03);
  border: 1px solid var(--glass-border);
  border-radius: 14px; padding: 1.05rem 1.15rem; margin: .35rem 0 .7rem;
}}
.verdict {{
  display: inline-block; font-size: .7rem; font-weight: 700;
  letter-spacing: .07em; text-transform: uppercase;
  padding: .3rem .62rem; border-radius: 8px;
}}
.v-strong   {{ color: #34d399; background: rgba(52,211,153,0.12);  border: 1px solid rgba(52,211,153,0.32); }}
.v-possible {{ color: #fbbf24; background: rgba(251,191,36,0.12);  border: 1px solid rgba(251,191,36,0.32); }}
.v-stretch  {{ color: #fb923c; background: rgba(251,146,60,0.12);  border: 1px solid rgba(251,146,60,0.32); }}
.v-no       {{ color: #f87171; background: rgba(248,113,113,0.12); border: 1px solid rgba(248,113,113,0.34); }}
.fit-summary {{ color: var(--text); font-size: .99rem; line-height: 1.5; margin: .7rem 0 0; }}
.fit-sec {{ margin-top: .85rem; }}
.fit-sec h4 {{
  font-size: .72rem; font-weight: 700; letter-spacing: .06em; text-transform: uppercase;
  color: var(--muted); margin: 0 0 .4rem;
}}
.fit-sec ul {{ list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: .32rem; }}
.fit-sec li {{ display: flex; gap: .55rem; align-items: flex-start; color: var(--text); font-size: .93rem; line-height: 1.45; }}
.fit-sec .ic {{ flex: 0 0 auto; font-weight: 800; line-height: 1.45; }}
.fit-sec ul.strengths .ic {{ color: var(--ok); }}
.fit-sec ul.gaps .ic     {{ color: #fb923c; }}
.fit-sec ul.improve .ic  {{ color: var(--accent-2); }}

/* Label above each draft email */
.draft-label {{
  font-size: .72rem; font-weight: 700; letter-spacing: .07em; text-transform: uppercase;
  color: var(--muted); margin: .2rem 0 .35rem;
}}

/* ── Result email cards ────────────────────────────────────────────────── */
[data-testid="stCode"] {{
  border-radius: 14px !important;
  border: 1px solid var(--glass-border);
  background: rgba(8,10,22,0.6) !important;
  backdrop-filter: blur(8px);
}}
.result-head {{
  display: flex; align-items: center; gap: .55rem;
  font-size: 1.12rem; font-weight: 700; color: var(--text);
  margin: 1.1rem 0 .2rem;
}}
.result-head .tag {{
  font-size: .68rem; font-weight: 600; letter-spacing: .08em; text-transform: uppercase;
  color: var(--accent-2); padding: .2rem .5rem; border-radius: 7px;
  background: rgba(139,116,61,0.14); border: 1px solid rgba(139,116,61,0.34);
}}

/* ── Alerts ────────────────────────────────────────────────────────────── */
[data-testid="stAlert"] {{
  border-radius: 13px;
  backdrop-filter: blur(10px);
  border: 1px solid var(--glass-border);
}}

/* ── Spinner text ──────────────────────────────────────────────────────── */
[data-testid="stSpinner"] p {{ color: var(--muted); font-weight: 500; }}

/* ── Divider + scrollbar ───────────────────────────────────────────────── */
hr {{ border-color: var(--glass-border); }}
::-webkit-scrollbar {{ width: 10px; height: 10px; }}
::-webkit-scrollbar-thumb {{ background: rgba(255,255,255,0.12); border-radius: 10px; }}
::-webkit-scrollbar-thumb:hover {{ background: rgba(139,116,61,0.55); }}
</style>
"""

HERO = """
<div class="hero">
  <h1>Land the reply, not the spam folder.</h1>
  <p>Add your résumé and a job link. We read your real experience and write a
     cold email grounded in it &mdash; no templates, no invented credentials.</p>
</div>
"""
