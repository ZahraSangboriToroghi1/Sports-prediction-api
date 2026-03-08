@echo off
chcp 65001 >nul
title Sports Prediction API - Running
color 0A
echo.
echo  =====================================================
echo    Sports Prediction API - Starting...
echo  =====================================================
echo.
echo  Open browser: http://localhost:8000/docs
echo  To stop:      CTRL + C
echo.
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
pause
