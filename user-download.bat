@echo off

set work= --remote
set diff= --diff
set game= --ipr

venv\Scripts\python.exe main.py %diff% %work% %game%
pause
