@echo off
:: ============================================================
:: PUSH.BAT - Save your changes to GitHub
:: Double-click this whenever you want to back up your work
:: ============================================================

cd /d "%~dp0.."

echo.
echo  Saving your work to GitHub...
echo  ==============================

:: Stage all changes
git add -A

:: Create a snapshot with today's date and time
git commit -m "Update: %DATE% %TIME%"

:: Push to GitHub
git push origin main

echo.
echo  Done! Your changes are saved to GitHub.
echo  Your other computers can now pull the latest.
echo.
pause
