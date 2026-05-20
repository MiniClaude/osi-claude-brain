# restore-memory.ps1
# Run this on a new computer after cloning osi-claude-brain.
# Copies backed-up memory files into the correct Cowork AppData folder.
#
# Usage: Right-click, Run with PowerShell
#        Or: powershell -ExecutionPolicy Bypass -File restore-memory.ps1

$memSrc = "$PSScriptRoot\memory"

if (-not (Test-Path $memSrc)) {
    Write-Host "ERROR: No memory folder found in repo. Make sure you cloned osi-claude-brain and ran git pull first." -ForegroundColor Red
    exit 1
}

# Find the Cowork auto-memory folder by searching for MEMORY.md in AppData
$memoryFile = Get-ChildItem "$env:APPDATA\Claude" -Recurse -Filter "MEMORY.md" -ErrorAction SilentlyContinue | Select-Object -First 1

if ($memoryFile) {
    $memDest = $memoryFile.DirectoryName
    Write-Host "Found Cowork memory folder: $memDest"
    Copy-Item "$memSrc\*" "$memDest\" -Force
    Write-Host "Memory restored successfully. $((Get-ChildItem $memDest).Count) files copied." -ForegroundColor Green
} else {
    Write-Host "Cowork memory folder not found in AppData." -ForegroundColor Yellow
    Write-Host "Open Cowork and start a conversation first, then re-run this script." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Manual fallback: copy the contents of the /memory folder from the repo"
    Write-Host "into: $env:APPDATA\Claude\local-agent-mode-sessions\...\memory\"
}
