"""
平台特定优化模块
"""

import sys

def get_platform() -> str:
    """获取当前平台"""
    if sys.platform.startswith('win'):
        return 'windows'
    elif sys.platform == 'darwin':
        return 'macos'
    elif sys.platform.startswith('linux'):
        return 'linux'
    elif sys.platform.startswith('android'):
        return 'android'
    else:
        return 'unknown'


def get_platform_optimizer():
    """获取平台优化器"""
    platform = get_platform()
    
    if platform == 'windows':
        from .windows_optimizer import WindowsOptimizer
        return WindowsOptimizer()
    elif platform == 'android':
        from .android_optimizer import AndroidOptimizer
        return AndroidOptimizer()
    else:
        from .base_optimizer import BaseOptimizer
        return BaseOptimizer()


__all__ = ['get_platform', 'get_platform_optimizer']
