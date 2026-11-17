@echo off
title StreamVault - Netflix OTT Frontend Prototype
echo ========================================================
echo   StreamVault - Netflix OTT Frontend Prototype (DBMS)
echo ========================================================
echo.
cd /d "%~dp0\netflix-frontend"

if exist ".venv\Scripts\streamlit.exe" (
    echo Starting Streamlit via .venv...
    ".venv\Scripts\streamlit.exe" run app.py
) else (
    echo Virtual environment not found in netflix-frontend\.venv.
    echo Trying global streamlit...
    streamlit run app.py
)
pause
