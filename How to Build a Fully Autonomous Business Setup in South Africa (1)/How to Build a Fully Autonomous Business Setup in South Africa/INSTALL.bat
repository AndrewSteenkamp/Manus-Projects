@echo off
echo ========================================
echo   AUTONOMOUS AI BUSINESS - INSTALLER
echo ========================================
echo.
echo This will install everything you need.
echo Please wait 2-3 minutes...
echo.

echo [1/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation!
    pause
    exit /b 1
)
echo Python found!
echo.

echo [2/4] Upgrading pip...
python -m pip install --upgrade pip --quiet
echo Done!
echo.

echo [3/4] Installing required packages...
echo This may take a minute...
pip install Flask openai requests python-dotenv --quiet
echo Done!
echo.

echo [4/4] Creating configuration file...
if not exist config.txt (
    echo OPENAI_API_KEY=YOUR_API_KEY_HERE > config.txt
    echo PAYFAST_MERCHANT_ID=10000100 >> config.txt
    echo PAYFAST_MERCHANT_KEY=46f0cd694581a >> config.txt
    echo PAYFAST_PASSPHRASE=jt7NOE43FZPn >> config.txt
    echo SANDBOX_MODE=true >> config.txt
    echo Configuration file created!
) else (
    echo Configuration file already exists.
)
echo.

echo ========================================
echo   INSTALLATION COMPLETE!
echo ========================================
echo.
echo NEXT STEPS:
echo 1. Edit config.txt and add your OpenAI API key
echo 2. Double-click START.bat to run the system
echo.
echo Press any key to close this window...
pause >nul
