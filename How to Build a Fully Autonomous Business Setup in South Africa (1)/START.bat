@echo off
echo ========================================
echo   AUTONOMOUS AI BUSINESS - STARTING
echo ========================================
echo.
echo Starting your AI business system...
echo.
echo The dashboard will open in your browser automatically.
echo.
echo To stop the system, close this window or press CTRL+C
echo.
echo ========================================
echo.

REM Load environment variables from config.txt
if exist config.txt (
    for /f "tokens=1,2 delims==" %%a in (config.txt) do (
        set %%a=%%b
    )
)

REM Start the Flask application
python app.py

pause
