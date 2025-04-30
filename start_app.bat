@echo off
REM === Activate conda and environment ===
CALL C:\Users\Administrator\anaconda3\Scripts\activate.bat deepseek

REM === Optional debugging (can remove these) ===

REM === Change directory to your project folder ===
cd /d D:\Moon\AI_Moon_Visibilty_Reporting\

REM === Start FastAPI server ===
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

