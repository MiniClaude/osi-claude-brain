@echo off
:: ============================================================
:: PULL.BAT - Get the latest from GitHub
:: Double-click this when you sit down at a different computer
:: ============================================================

cd /d "%~dp0.."

echo.
echo  Grabbing the latest from GitHub...
echo  ====================================

git pull origin main

echo.
echo  Done! You have the latest version of everything.
echo.
pause
