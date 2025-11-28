@echo off
title SpeakerLove AI - Launcher
cls

echo.
echo ================================================
echo   SpeakerLove AI - Voice Isolation Launcher
echo ================================================
echo.

:: Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found!
    echo Please install Python 3.8+ from https://www.python.org/
    echo.
    pause
    exit /b 1
)

echo Python found: 
python --version
echo.

:: Try to ensure dependencies are installed (but don't fail if already installed)
echo Checking/installing dependencies...
pip install -r requirements.txt >nul 2>&1

echo.
echo Starting SpeakerLove AI...
echo ================================================
echo.

:: Run the application
python SpeakerLove.py

:: If the app crashes, keep the window open to see the error
if %errorlevel% neq 0 (
    echo.
    echo ================================================
    echo [ERROR] Application exited with error
    echo ================================================
    echo.
    pause
)
