@echo off
REM Auto-commit and push Claude-Brain changes.
REM Runs from Windows Task Scheduler, NOT from Cowork.
REM Avoids the .git/index.lock sandbox permission bug.

cd /d C:\Claude-Brain

REM Pull first so we don't push over the other laptop's work.
git pull --quiet
if errorlevel 1 (
    echo [%date% %time%] PULL FAILED, skipping push >> C:\Claude-Brain\auto-push.log
    exit /b 1
)

REM Stage everything.
git add .

REM Skip commit if nothing changed.
git diff --staged --quiet
if not errorlevel 1 (
    echo [%date% %time%] no changes >> C:\Claude-Brain\auto-push.log
    exit /b 0
)

REM Commit + push.
git commit -m "auto-push %date% %time%" --quiet
git push --quiet
if errorlevel 1 (
    echo [%date% %time%] PUSH FAILED >> C:\Claude-Brain\auto-push.log
    exit /b 1
)

echo [%date% %time%] pushed >> C:\Claude-Brain\auto-push.log
exit /b 0
