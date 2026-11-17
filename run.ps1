# StreamVault - Netflix OTT Prototype Launcher
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  StreamVault - Netflix OTT Frontend Prototype (DBMS)" -ForegroundColor Red
Write-Host "========================================================" -ForegroundColor Cyan

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location "$scriptDir\netflix-frontend"

$venvStreamlit = "$scriptDir\netflix-frontend\.venv\Scripts\streamlit.exe"

if (Test-Path $venvStreamlit) {
    Write-Host "Starting Streamlit via local virtual environment..." -ForegroundColor Green
    & $venvStreamlit run app.py
} else {
    Write-Host "Virtual environment not detected. Running system streamlit..." -ForegroundColor Yellow
    streamlit run app.py
}
