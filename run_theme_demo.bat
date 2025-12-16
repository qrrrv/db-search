@echo off
chcp 65001 >nul 2>&1
cd /d "%~dp0"
title Theme Demo - DB Search Tool

echo.
echo ============================================================
echo            THEME DEMO
echo ============================================================
echo.

python -c "
from modules.themes.color_schemes import ColorSchemes
from modules.themes.ascii_art import ASCIIArt

print('Available Themes:')
print('=' * 50)

for name in ColorSchemes.list_schemes():
    scheme = ColorSchemes.get_scheme(name)
    print(f'  {name}: {scheme.get(\"name\", name)}')
    print(f'    Primary: {scheme[\"primary\"]}')
    print(f'    Secondary: {scheme[\"secondary\"]}')
    print()

print()
print('ASCII Art Demo:')
print('=' * 50)
print(ASCIIArt.generate_banner('DEMO', 'slant'))
"

echo.
pause