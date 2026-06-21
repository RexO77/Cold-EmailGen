# Cold Mail Generator - Windows launcher (PowerShell)
#
#   .\run.ps1            -> set up if needed, then start the app
#   $env:PORT=8600; .\run.ps1   -> start on a different port
#
# Idempotent: creates the venv + installs deps on first run, and reinstalls
# only when requirements.txt changes. Otherwise it goes straight to the server.
# Tip: if you get "running scripts is disabled", launch via run.bat instead.

$ErrorActionPreference = "Stop"
Set-Location -Path $PSScriptRoot

$Venv  = ".venv"
$Py    = ".\$Venv\Scripts\python.exe"
$Stamp = "$Venv\.requirements.sha256"
$Port  = if ($env:PORT) { $env:PORT } else { "8501" }

function Say($msg) { Write-Host "> $msg" -ForegroundColor Yellow }

# 1. Create the virtualenv with a compatible Python (3.11-3.13; 3.14+ can't
#    build the pinned deps). Prefer the 'py' launcher to pick an exact version.
if (-not (Test-Path $Py)) {
    $baseCmd = $null; $baseArgs = @()
    foreach ($v in @("3.13", "3.12", "3.11")) {
        try { & py "-$v" --version *> $null; if ($LASTEXITCODE -eq 0) { $baseCmd = "py"; $baseArgs = @("-$v"); break } } catch {}
    }
    if (-not $baseCmd) {
        try {
            $ver = & python -c "import sys;print('%d.%d' % sys.version_info[:2])" 2>$null
            if ($ver -match '^3\.(11|12|13)$') { $baseCmd = "python"; $baseArgs = @() }
        } catch {}
    }
    if (-not $baseCmd) {
        Write-Host "X Need Python 3.11-3.13 (3.14+ can't build the pinned deps)." -ForegroundColor Red
        Write-Host "  Install it from https://www.python.org/downloads/ and tick 'Add python.exe to PATH'." -ForegroundColor Red
        exit 1
    }
    Say "Creating virtualenv ($baseCmd $baseArgs)"
    & $baseCmd @baseArgs -m venv $Venv
}

# 2. Install/refresh deps only when requirements.txt changed.
$want = (Get-FileHash requirements.txt -Algorithm SHA256).Hash
$have = if (Test-Path $Stamp) { Get-Content $Stamp -Raw } else { "none" }
if ($want -ne $have.Trim()) {
    Say "Installing dependencies"
    & $Py -m pip install --quiet --upgrade pip
    & $Py -m pip install --quiet -r requirements.txt
    Set-Content -Path $Stamp -Value $want
} else {
    Say "Dependencies already up to date"
}

# 3. Make sure an .env exists (the app needs GROQ_API_KEY).
if (-not (Test-Path "App\.env")) {
    Copy-Item "App\.env.example" "App\.env"
    Write-Host "! Created App\.env from the template - add your GROQ_API_KEY to it." -ForegroundColor Yellow
    Write-Host "  Get one at https://console.groq.com/keys" -ForegroundColor Yellow
}
if (Select-String -Path "App\.env" -Pattern "your_groq_api_key_here" -Quiet) {
    Write-Host "! App\.env still has the placeholder key - email generation will fail until you set a real GROQ_API_KEY." -ForegroundColor Yellow
}

# 4. Start the server.
Say "Starting Cold Mail Generator on http://localhost:$Port"
& $Py -m streamlit run App/main.py --server.port $Port
