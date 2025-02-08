@echo off
rem hallo
powershell -Command "Start-Process powershell -ArgumentList '-NoExit', '-Command', 'python ./src/aurora.py' -WindowStyle Normal"
exit
