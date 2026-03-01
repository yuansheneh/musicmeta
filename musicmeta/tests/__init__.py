"""
MusicMeta 测试套件
"""

import unittest
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def run_all_tests():
    """运行所有测试"""
    from test_core import run_tests as run_core_tests
    
    print("=" * 60)
    print("MusicMeta 测试套件")
    print("=" * 60)
    print()
    
    # 运行核心测试
    print("运行核心功能测试...")
    core_success = run_core_tests()
    
    print()
    print("=" * 60)
    
    if core_success:
        print("✓ 所有测试通过!")
        return True
    else:
        print("✗ 部分测试失败")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
