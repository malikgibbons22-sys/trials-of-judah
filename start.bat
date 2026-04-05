@echo off
title Trials of Judah
color 0A

echo.
echo  ==========================================
echo    Trials of Judah — Starting...
echo  ==========================================
echo.

cd /d "%~dp0"

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Install from https://python.org
    pause
    exit /b 1
)

:: Install deps (quiet, idempotent)
pip install -r backend\requirements.txt --quiet 2>nul

:: Launch browser + server
start "" cmd /c "timeout /t 2 /nobreak >nul && start http://localhost:8202"
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8202

pause
