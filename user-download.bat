@echo off

set diff= --remote
set work= --diff
set game= --ipr

venv\Scripts\python.exe main.py %diff% %work% %game%
pause
