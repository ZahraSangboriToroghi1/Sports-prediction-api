@echo off
chcp 65001 >nul
title Sports Prediction API - Setup
color 0B
echo.
echo  =====================================================
echo    Sports Prediction API - First Time Setup
echo  =====================================================
echo.
echo  Run this file ONCE only.
echo  After done, use BASLAT.bat every time.
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found!
    echo Please install Python 3.10+ from python.org
    pause
    exit
)

echo [1/3] Installing libraries (Python 3.13 compatible)...
pip install "numpy>=2.0.0" "pandas>=2.2.3" "scikit-learn>=1.5.2" "xgboost>=2.1.1" "fastapi==0.115.0" "uvicorn==0.30.0" "requests==2.32.3" "slowapi==0.1.9"
if %errorlevel% neq 0 (
    echo [ERROR] Install failed. Check internet.
    pause
    exit
)

echo.
echo [2/3] Downloading data and training ML model...
echo       This takes 5-10 minutes, please wait!
echo.
python train.py
if %errorlevel% neq 0 (
    echo [ERROR] Training failed.
    pause
    exit
)

echo.
echo  =====================================================
echo    Done! Now double-click BASLAT.bat
echo  =====================================================
echo.
pause
