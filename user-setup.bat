@echo off

uv venv venv
call venv\Scripts\activate
uv pip install -r requirements.txt

echo Installation Finished!
pause
