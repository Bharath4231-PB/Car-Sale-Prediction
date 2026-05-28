@echo off
REM ============================================================
REM Car Sales Price Prediction System - Quick Start Guide
REM ============================================================

ECHO.
ECHO ============================================================
ECHO  Car Sales Price Prediction System - SETUP
ECHO ============================================================
ECHO.

REM Step 1: Check Python
ECHO [1/5] Checking Python installation...
python --version
IF ERRORLEVEL 1 (
    ECHO ERROR: Python not found. Please install Python 3.8+
    PAUSE
    EXIT /B 1
)

REM Step 2: Navigate to project directory
ECHO.
ECHO [2/5] Navigating to project directory...
CD /D e:\car sales prediction\car_sales_prediction
IF ERRORLEVEL 1 (
    ECHO ERROR: Cannot find project directory
    PAUSE
    EXIT /B 1
)

REM Step 3: Install dependencies
ECHO.
ECHO [3/5] Installing Python packages...
ECHO Please wait, this may take a minute...
pip install -r requirements.txt --quiet
IF ERRORLEVEL 1 (
    ECHO WARNING: Some packages may not have installed correctly
)

REM Step 4: Verify MySQL (informational)
ECHO.
ECHO [4/5] MySQL Setup Instructions:
ECHO ============================================================
ECHO 1. Ensure MySQL is running:
ECHO    - Windows: net start MySQL80
ECHO    - Or use MySQL Workbench
ECHO.
ECHO 2. Create database:
ECHO    - Open MySQL Workbench or Command Prompt
ECHO    - mysql -u root -pben10 -e "source database.sql"
ECHO ============================================================

ECHO.
ECHO [5/5] Next Steps:
ECHO ============================================================
ECHO.
ECHO Run these commands in order:
ECHO.
ECHO 1. Train the ML Model (ONE TIME ONLY):
ECHO    python train_model.py
ECHO.
ECHO 2. Start the Flask Server:
ECHO    python app.py
ECHO.
ECHO 3. Open Browser:
ECHO    http://127.0.0.1:5000
ECHO.
ECHO ============================================================
ECHO.
PAUSE
