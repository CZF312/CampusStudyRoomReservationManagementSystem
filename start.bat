REM 【F1-1·步骤1】实例：组长双击本文件，调用 scripts\start-system.ps1 启动系统
@echo off
setlocal
chcp 65001 >nul 2>&1
cd /d "%~dp0"
title Campus Study Room Reservation System

if not exist "pom.xml" (
    echo [ERROR] pom.xml not found. Run this file from the project root directory.
    pause
    exit /b 1
)

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
