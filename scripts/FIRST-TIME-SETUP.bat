@echo off
:: ============================================================
:: FIRST-TIME-SETUP.BAT
:: Run this ONCE on your main computer to connect to GitHub
:: ============================================================

echo.
echo  ==========================================
echo   OSI Claude Brain - First Time Setup
echo  ==========================================
echo.

:: Go to the repo folder (one level up from scripts/)
cd /d "%~dp0.."

echo  Step 1: Setting your Git identity...
git config user.name "Brian Charrette"
git config user.email "bc@osihardware.com"
git config --global init.defaultBranch main
echo  Done.
echo.

echo  Step 2: Initializing Git in this folder...
git init
git branch -M main
echo  Done.
echo.

echo  Step 3: Now we need your GitHub repo URL.
echo.
echo  Go to github.com and:
echo    1. Create a NEW repo named: osi-claude-brain
echo    2. Set it to PRIVATE
echo    3. Do NOT check "Initialize with README"
echo    4. After creating it, copy the repo URL
echo       (looks like: https://github.com/YOURNAME/osi-claude-brain.git)
echo.
set /p REPO_URL="  Paste your GitHub repo URL here and press Enter: "

echo.
echo  Step 4: Connecting this folder to GitHub...
git remote add origin %REPO_URL%
echo  Done.
echo.

echo  Step 5: Saving everything and pushing to GitHub...
git add -A
git commit -m "First upload — OSI Claude Brain setup"
git push -u origin main

echo.
echo  ==========================================
echo   Setup Complete!
echo  ==========================================
echo.
echo  When asked for username/password:
echo    Username = your GitHub username
echo    Password = your Personal Access Token
echo              (NOT your GitHub password!)
echo.
echo  If you don't have a token yet, see docs\SETUP.md Step 5.
echo.
pause
