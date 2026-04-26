@echo off
REM Quick Start Script for Azure Event Hub Web Application (Windows)

echo.
echo ==========================================
echo Azure Event Hub Web Application
echo Quick Start Setup
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org
    pause
    exit /b 1
)

echo Python found:
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Check if .env file exists
if not exist ".env" (
    echo.
    echo WARNING: .env file not found!
    echo Creating .env from .env.example...
    copy .env.example .env
    echo.
    echo Please edit .env and add your Azure Event Hub credentials:
    echo   - EVENT_HUB_CONNECTION_STRING
    echo   - EVENT_HUB_NAME
) else (
    echo .env file found
)

echo.
echo ==========================================
echo Setup complete!
echo ==========================================
echo.
echo To start the application, run:
echo   python app.py
echo.
echo Then open your browser to:
echo   http://localhost:5000
echo.
pause
