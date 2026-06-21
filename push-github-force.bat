@echo off
setlocal
chcp 65001 >nul 2>&1
cd /d "%~dp0"
title Push CSRRM V3.0 to GitHub

echo ========================================
echo  Force push to CZF312/master
echo  CampusStudyRoomReservationManagementSystem
echo ========================================
echo.

git remote set-url origin https://github.com/CZF312/CampusStudyRoomReservationManagementSystem.git
git status -sb
echo.
git push --force -u origin main:master
set ERR=%ERRORLEVEL%

echo.
if %ERR% NEQ 0 (
    echo [ERROR] Push failed. Check GitHub login or network.
) else (
    echo [OK] https://github.com/CZF312/CampusStudyRoomReservationManagementSystem
)
pause
exit /b %ERR%
