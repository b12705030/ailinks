@echo off
REM Windows 批处理脚本：批量更新所有链接的 short_name

echo ==================================================
echo 批量更新所有链接的 short_name
echo ==================================================
echo.

REM 切换到 backend 目录
cd /d "%~dp0\.."

REM 激活虚拟环境
if exist "venv\Scripts\activate.bat" (
    echo 激活虚拟环境...
    call venv\Scripts\activate.bat
) else (
    echo 警告：未找到虚拟环境，使用系统 Python
)

REM 运行脚本
echo 开始运行更新脚本...
echo.
python scripts\update_short_names.py

pause

