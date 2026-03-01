@echo off
REM MusicMeta Windows 启动脚本

cd /d "%~dp0"

REM 检查 Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python 未安装！请安装 Python 3.8+
    pause
    exit /b 1
)

REM 检查依赖
echo 检查依赖...
pip install -r requirements.txt -q

REM 启动应用
echo 启动 MusicMeta...
python run.py

pause
