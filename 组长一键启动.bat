@echo off
setlocal
chcp 65001 >nul 2>&1
cd /d "%~dp0"
title Campus Study Room Reservation System

if not exist "pom.xml" (
    echo [ERROR] pom.xml not found. Run from project root.
    pause
    exit /b 1
)

echo [INFO] Legacy launcher redirected to start-system.ps1
echo        Prefer start.bat in project root.
echo.

set "CSRRM_SCRIPT_ROOT=%~dp0scripts"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\start-system.ps1"
set ERR=%ERRORLEVEL%

echo.
if %ERR% NEQ 0 (
    echo [ERROR] Setup failed. Exit code %ERR%.
) else (
    echo Setup finished.
)
pause
exit /b %ERR%
