@echo off
chcp 65001 >nul 2>&1
cd /d "%~dp0"
title Installing Dependencies - DB Search Tool v2.0

echo.
echo ============================================================
echo            INSTALLING DEPENDENCIES
echo            DB Search Tool v2.0 PRO
echo ============================================================
echo.

where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found!
    echo.
    echo Download from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo [OK] Python found:
python --version
echo.

echo [*] Upgrading pip...
python -m pip install --upgrade pip
echo.

echo [*] Installing libraries...
echo.

echo [1/12] Installing Rich (beautiful console)...
pip install rich

echo [2/12] Installing Colorama (Windows colors)...
pip install colorama

echo [3/12] Installing Prompt Toolkit (enhanced input)...
pip install prompt_toolkit

echo [4/12] Installing Pyfiglet (ASCII art)...
pip install pyfiglet

echo [5/12] Installing ART (more ASCII art)...
pip install art

echo [6/12] Installing TQDM (progress bars)...
pip install tqdm

echo [7/12] Installing Alive-Progress (animated progress)...
pip install alive-progress

echo [8/12] Installing Halo (spinners)...
pip install halo

echo [9/12] Installing Tabulate (tables)...
pip install tabulate

echo [10/12] Installing Blessed (terminal)...
pip install blessed

echo [11/12] Installing Click (CLI)...
pip install click

echo [12/12] Installing Chardet (encoding detection)...
pip install chardet

echo.
echo ============================================================
echo            INSTALLATION COMPLETE!
echo ============================================================
echo.
echo Libraries installed:
echo   - Rich (beautiful console output)
echo   - Colorama (Windows color support)
echo   - Prompt Toolkit (enhanced input)
echo   - Pyfiglet (ASCII art banners)
echo   - ART (more ASCII art fonts)
echo   - TQDM (progress bars)
echo   - Alive-Progress (animated progress)
echo   - Halo (spinners)
echo   - Tabulate (table formatting)
echo   - Blessed (terminal control)
echo   - Click (CLI framework)
echo   - Chardet (encoding detection)
echo.
echo Now run start.bat to launch the program
echo Put your databases (.txt, .csv) into "bd" folder
echo.
pause