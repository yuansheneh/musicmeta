#!/usr/bin/env python3
"""
MusicMeta 启动脚本
"""

import sys
import os

# 添加 src 到路径
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.insert(0, src_path)

from main import main

if __name__ == "__main__":
    main()
