@echo off
setlocal enabledelayedexpansion

title Gemini in Chrome Enabler - Windows Setup

echo ====================================================
echo       Gemini in Chrome Enabler - Windows Setup
echo ====================================================

REM 1. 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] 未检测到 Python，请先从 https://www.python.org/ 安装 Python。
    echo 请确保在安装时勾选 "Add Python to PATH"。
    pause
    exit /b
)

REM 2. 安装必要依赖 (psutil)
echo [1/3] 正在检查环境依赖...
python -m pip install psutil --quiet
if errorlevel 1 (
    echo [WARNING] 依赖安装失败，但这不影响主要功能，继续执行...
) else (
    echo [OK] 环境依赖就绪
)

REM 3. 执行修复脚本
echo [2/3] 正在启动主修复程序...
python "%~dp0enable_gemini_win.py"

echo.
echo ====================================================
echo [DONE] 操作已完成！
echo ====================================================
echo.
pause
