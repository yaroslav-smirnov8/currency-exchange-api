@echo off
setlocal
python -m pytest -q --color=yes
exit /b %errorlevel%
