@echo off
echo Installing SpeakerLove...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo Installing required packages...
pip install -r requirements.txt

if errorlevel 1 (
    echo Error: Failed to install packages
    pause
    exit /b 1
)

echo.
echo Installation complete!
echo You can now run: python voice_isolator.py
echo.
pause
