@echo off
setlocal

call "%~dp0venv\Scripts\activate.bat" 2>nul
if errorlevel 1 (
    echo [ERROR] Cannot activate venv. Run: python -m venv venv
    pause
    exit /b 1
)

python "%~dp0main.py"
pause
