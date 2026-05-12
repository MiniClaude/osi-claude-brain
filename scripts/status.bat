@echo off
:: ============================================================
:: STATUS.BAT - See what files have changed since last push
:: ============================================================

cd /d "%~dp0.."

echo.
echo  What's changed since your last save:
echo  ======================================
git status

echo.
echo  Recent saves (newest first):
echo  ==============================
git log --oneline -10

echo.
pause
