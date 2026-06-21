@echo off
REM 【F1-1·环境启动】功能链实例：组长双击 start.bat → PowerShell 导入 database-full.sql 建库 → Spring Boot 8080 → 浏览器登录页
REM 【行】关闭命令回显，保持终端输出简洁
setlocal & REM 【行】执行本行语句，推进功能链中的当前步骤
REM 【行】切换控制台为 UTF-8，避免中文乱码
chcp 65001 >nul 2>&1 & REM 【行】执行本行语句，推进功能链中的当前步骤
REM 【行】进入 bat 所在目录（项目根），保证相对路径正确
cd /d "%~dp0" & REM 【行】执行本行语句，推进功能链中的当前步骤
title Campus Study Room Reservation System & REM 【行】执行本行语句，推进功能链中的当前步骤

REM 【行】校验 pom.xml 存在，防止在错误目录双击
if not exist "pom.xml" ( & REM 【行】执行本行语句，推进功能链中的当前步骤
    echo [ERROR] pom.xml not found. Run this file from the project root directory. & REM 【行】执行本行语句，推进功能链中的当前步骤
    pause & REM 【行】执行本行语句，推进功能链中的当前步骤
    exit /b 1 & REM 【行】执行本行语句，推进功能链中的当前步骤
)

REM 【行】告知 PowerShell 脚本所在目录
set "CSRRM_SCRIPT_ROOT=%~dp0scripts" & REM 【行】执行本行语句，推进功能链中的当前步骤
REM 【行】调用一键启动脚本：建库、编译、启动 Spring Boot、打开浏览器
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\start-system.ps1" & REM 【行】执行本行语句，推进功能链中的当前步骤
set ERR=%ERRORLEVEL% & REM 【行】执行本行语句，推进功能链中的当前步骤

echo. & REM 【行】执行本行语句，推进功能链中的当前步骤
REM 【行】根据 PowerShell 退出码提示成功或失败
if %ERR% NEQ 0 ( & REM 【行】执行本行语句，推进功能链中的当前步骤
    echo [ERROR] Setup failed. Exit code %ERR%. & REM 【行】执行本行语句，推进功能链中的当前步骤
) else ( & REM 【行】执行本行语句，推进功能链中的当前步骤
    echo Setup finished. & REM 【行】执行本行语句，推进功能链中的当前步骤
)
pause & REM 【行】执行本行语句，推进功能链中的当前步骤
exit /b %ERR% & REM 【行】执行本行语句，推进功能链中的当前步骤
