@echo off
echo Starting local server...
start /B pythonw serve.py
timeout /t 2 /nobreak >nul
start "" http://localhost:8765/project_scope_form.html
