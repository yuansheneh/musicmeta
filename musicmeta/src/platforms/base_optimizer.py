"""
基础优化器 - 默认实现
"""

from typing import Optional, List


class BaseOptimizer:
    """基础平台优化器"""
    
    def __init__(self):
        self.platform = "base"
    
    def initialize(self):
        """初始化平台特定功能"""
        pass
    
    def cleanup(self):
        """清理资源"""
        pass
    
    def get_music_folders(self) -> List[str]:
        """获取默认音乐文件夹列表"""
        import os
        from pathlib import Path
        
        home = Path.home()
        default_folders = [
            str(home / "Music"),
            str(home / "Muziek"),
            str(home / "Musique"),
            str(home / "Musik"),
            str(home / "Música"),
        ]
        
        return [f for f in default_folders if os.path.exists(f)]
    
    def register_file_handler(self, extension: str):
        """注册文件处理器"""
        pass
    
    def unregister_file_handler(self, extension: str):
        """注销文件处理器"""
        pass
    
    def show_in_file_manager(self, file_path: str):
        """在文件管理器中显示文件"""
        pass
    
    def set_taskbar_progress(self, progress: float):
        """设置任务栏进度"""
        pass
    
    def enable_dark_titlebar(self, window):
        """启用暗色标题栏"""
        pass
    
    def get_system_theme(self) -> str:
        """获取系统主题"""
        return "dark"
    
    def optimize_for_touch(self):
        """优化触摸交互"""
        pass
    
    def optimize_for_high_dpi(self):
        """优化高 DPI 显示"""
        pass
