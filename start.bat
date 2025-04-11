@echo off
rem echo HTTP-Server wird gestartet...
start "" uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload
timeout /t 4 >NUL
start http://127.0.0.1:8002
