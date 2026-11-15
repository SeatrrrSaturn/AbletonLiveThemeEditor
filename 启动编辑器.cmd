@echo off
chcp 65001 >nul
set "PY=%LOCALAPPDATA%\Microsoft\WindowsApps\pythonw.exe"
if not exist "%PY%" set "PY=%LOCALAPPDATA%\Microsoft\WindowsApps\python.exe"
start "" "%PY%" "%~dp0live_theme_editor.py"