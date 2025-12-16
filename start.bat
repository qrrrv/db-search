@echo off
chcp 65001 >nul 2>&1
cd /d "%~dp0"
title DB Search Tool v2.0 PRO

echo.
echo ============================================================
echo            DATABASE SEARCH TOOL v2.0 PRO
echo            Starting...
echo ============================================================
echo.

where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found!
    echo.
    echo Please install Python 3.8 or higher
    echo Download: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [OK] Python found
python --version
echo.
echo Starting program...
echo.

python "%~dp0main.py"

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Program crashed with error code %errorlevel%
)

pause
