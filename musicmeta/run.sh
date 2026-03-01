#!/bin/bash
# MusicMeta Linux/Mac 启动脚本

cd "$(dirname "$0")"

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "Python3 未安装！请安装 Python 3.8+"
    exit 1
fi

# 检查依赖
echo "检查依赖..."
pip3 install -r requirements.txt -q

# 启动应用
echo "启动 MusicMeta..."
python3 run.py
