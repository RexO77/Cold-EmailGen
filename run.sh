#!/usr/bin/env bash
#
# One command to rule them all.
#   ./run.sh            → set up if needed, then start the app
#   PORT=8600 ./run.sh  → start on a different port
#
# Idempotent: creates the venv + installs deps on first run, and reinstalls
# only when requirements.txt changes. Otherwise it goes straight to the server.

set -euo pipefail
cd "$(dirname "$0")"

VENV=".venv"
PY="$VENV/bin/python"
PORT="${PORT:-8501}"
STAMP="$VENV/.requirements.sha256"

say() { printf '\033[1;33m▸ %s\033[0m\n' "$1"; }

# 1. Pick a compatible interpreter (deps don't build on Python 3.14+).
pick_python() {
  for c in python3.13 python3.12 python3.11 python3; do
    if command -v "$c" >/dev/null 2>&1; then
      ver="$("$c" -c 'import sys; print("%d.%d" % sys.version_info[:2])')"
      major="${ver%%.*}"; minor="${ver##*.}"
      if [ "$major" -eq 3 ] && [ "$minor" -ge 11 ] && [ "$minor" -le 13 ]; then
        echo "$c"; return 0
      fi
    fi
  done
  return 1
}

# 2. Create the virtualenv if it doesn't exist.
if [ ! -x "$PY" ]; then
  if ! BASE_PY="$(pick_python)"; then
    echo "✗ Need Python 3.11–3.13 (3.14+ can't build the pinned deps)." >&2
    echo "  Install one, e.g.:  brew install python@3.13" >&2
    exit 1
  fi
  say "Creating virtualenv with $BASE_PY"
  "$BASE_PY" -m venv "$VENV"
fi

# 3. Install/refresh deps only when requirements.txt changed.
WANT="$(shasum -a 256 requirements.txt | awk '{print $1}')"
HAVE="$(cat "$STAMP" 2>/dev/null || echo none)"
if [ "$WANT" != "$HAVE" ]; then
  say "Installing dependencies"
  "$PY" -m pip install --quiet --upgrade pip
  "$PY" -m pip install --quiet -r requirements.txt
  echo "$WANT" > "$STAMP"
else
  say "Dependencies already up to date"
fi

# 4. Make sure an .env exists (the app needs GROQ_API_KEY).
if [ ! -f App/.env ]; then
  cp App/.env.example App/.env
  echo "⚠  Created App/.env from the template — add your GROQ_API_KEY to it."
  echo "   Get one at https://console.groq.com/keys"
fi
if grep -q "your_groq_api_key_here" App/.env 2>/dev/null; then
  echo "⚠  App/.env still has the placeholder key — email generation will fail until you set a real GROQ_API_KEY."
fi

# 5. Start the server.
say "Starting Cold Mail Generator on http://localhost:$PORT"
exec "$PY" -m streamlit run App/main.py --server.port "$PORT"
