@echo off

set diff= --diff
set game= --ipr
set work= --remote

venv\Scripts\python.exe main.py %diff% %game% %work%
pause
