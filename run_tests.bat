@echo off
setlocal

:: Enable ANSI escape sequences in cmd on Windows 10+
for /f %%A in ('echo prompt $E ^| cmd') do set "ESC=%%A"
>nul reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f

:: Activate virtual environment
call "%~dp0venv\Scripts\activate.bat" 2>nul
if errorlevel 1 (
    echo [ERROR] Cannot activate venv. Run: python -m venv venv
    pause
    exit /b 1
)

:: Run the Python test runner for pretty green output
python "%~dp0run_tests.py"
pause
exit /b %errorlevel%
