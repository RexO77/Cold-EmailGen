# Running on Windows 🪟

A step-by-step guide to run the Cold Mail Generator on Windows without the usual errors.

## 1. Install Python 3.13

> **This is the #1 cause of install errors.** The dependencies ship prebuilt wheels for
> Python **3.11–3.13 only**. On **Python 3.14+**, pip tries to compile packages like
> `pandas`/`chromadb` from source and fails (you'll see *"Microsoft Visual C++ 14.0 or
> greater is required"* or a long red build traceback). Use 3.13.

1. Download Python 3.13 from <https://www.python.org/downloads/>.
2. In the installer, **tick "Add python.exe to PATH"**.
3. Verify in a new terminal:
   ```powershell
   py -3.13 --version
   ```
   It should print `Python 3.13.x`.

## 2. Get the code

```powershell
git clone https://github.com/RexO77/Cold-EmailGen.git
cd Cold-EmailGen
```

(No Git? Download the ZIP from the GitHub page → **Code ▸ Download ZIP**, then extract it.)

## 3. Run it (one command)

**Easiest:** double-click **`run.bat`** in File Explorer.

Or from a terminal:

```powershell
.\run.bat
```

The first run creates a virtual environment, installs everything, and starts the app.
Later runs skip setup and launch straight away. When it's ready, open
**http://localhost:8501**.

> Different port: `set PORT=8600` (cmd) or `$env:PORT=8600` (PowerShell), then `.\run.bat`.

## 4. Add your Groq API key

The app uses **Groq** for the AI. The first run creates `App\.env` from the template —
open it in Notepad and set your key:

```
GROQ_API_KEY=your_groq_api_key
```

Get a free key at <https://console.groq.com/keys>. Save the file and refresh the app.
(Until you set a real key, email generation fails with a "rate limit / invalid key" message.)

---

## Manual setup (if you prefer not to use the script)

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy App\.env.example App\.env       REM then edit App\.env and add your key
streamlit run App/main.py
```

In **cmd** (not PowerShell), activate with `.\.venv\Scripts\activate.bat` instead.

---

## Troubleshooting

| Error you see | Cause | Fix |
|---|---|---|
| *"Microsoft Visual C++ 14.0 is required"* or a long build traceback during `pip install` | You're on **Python 3.14+** — no prebuilt wheels | Install **Python 3.13** (step 1) and delete the `.venv` folder, then re-run |
| `running scripts is disabled on this system` (PowerShell) | Execution policy blocks `.ps1` | Use **`run.bat`** (it bypasses this), or run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once |
| `'py' is not recognized` / `'python' is not recognized` | Python not installed or not on PATH | Reinstall Python and tick **"Add python.exe to PATH"**, then open a **new** terminal |
| `Port 8501 is in use` | Another instance is still running | Close the old terminal, or start on another port: `$env:PORT=8600; .\run.bat` |
| `streamlit: command not found` | Running outside the venv | Use `run.bat`, or activate the venv first (manual setup above) |
| App opens but generation fails with rate-limit / key error | `GROQ_API_KEY` missing or placeholder | Set a real key in `App\.env` (step 4) |
| `ModuleNotFoundError` after pulling new code | `requirements.txt` changed | Just re-run `run.bat` — it reinstalls automatically when deps change |
| Filename / "path too long" errors | Windows long-path limit | Clone into a short path like `C:\dev\Cold-EmailGen`, or enable long paths |

Still stuck? Open an issue with the full error text from the terminal.
