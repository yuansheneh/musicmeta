"""
Windows 平台特殊优化
- 文件资源管理器集成
- 右键菜单支持
- 任务栏进度
- 高分屏 DPI 适配
- 暗色标题栏
"""

import os
import sys
from typing import Optional, List
from pathlib import Path

from .base_optimizer import BaseOptimizer


class WindowsOptimizer(BaseOptimizer):
    """Windows 平台优化器"""
    
    def __init__(self):
        super().__init__()
        self.platform = "windows"
        self.taskbar_lib = None
        
        # 尝试导入 Windows 特定库
        try:
            import ctypes
            self.user32 = ctypes.windll.user32
            self.dwmapi = ctypes.windll.dwmapi
        except Exception:
            pass
    
    def initialize(self):
        """初始化 Windows 特定功能"""
        # 启用 DPI 感知
        self.optimize_for_high_dpi()
        
        # 尝试导入任务栏库
        try:
            from comtypes import CLSCTX_ALL
            from ctypes import cast, POINTER
            # 这里可以集成 Windows 任务栏 API
        except Exception:
            pass
    
    def get_music_folders(self) -> List[str]:
        """获取 Windows 音乐文件夹"""
        try:
            import ctypes.wintypes
            from ctypes import windll
            
            # 获取用户音乐文件夹路径
            CSIDL_MYMUSIC = 13
            MAX_PATH = 260
            
            buf = ctypes.create_unicode_buffer(MAX_PATH)
            windll.shell32.SHGetFolderPathW(None, CSIDL_MYMUSIC, None, 0, buf)
            
            folders = [buf.value]
            
            # 添加公共音乐文件夹
            CSIDL_COMMON_MUSIC = 53
            buf2 = ctypes.create_unicode_buffer(MAX_PATH)
            result = windll.shell32.SHGetFolderPathW(None, CSIDL_COMMON_MUSIC, None, 0, buf2)
            if result == 0:
                folders.append(buf2.value)
            
            return [f for f in folders if os.path.exists(f)]
            
        except Exception:
            return super().get_music_folders()
    
    def register_file_handler(self, extension: str):
        """在 Windows 注册文件处理器（右键菜单）"""
        try:
            import winreg
            
            # 注册到右键菜单
            key_path = f"Software\\Classes\\{extension}\\shell\\MusicMeta"
            
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
                winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "用 MusicMeta 编辑")
            
            # 添加图标
            icon_path = os.path.abspath(sys.argv[0])
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"{key_path}\\command") as key:
                cmd = f'python "{os.path.abspath(sys.argv[0])}" "%1"'
                winreg.SetValueEx(key, "", 0, winreg.REG_SZ, cmd)
                
        except Exception as e:
            print(f"注册文件处理器失败：{e}")
    
    def unregister_file_handler(self, extension: str):
        """注销文件处理器"""
        try:
            import winreg
            
            key_path = f"Software\\Classes\\{extension}\\shell\\MusicMeta"
            
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
                    winreg.DeleteKey(key, "command")
                winreg.DeleteKey(winreg.HKEY_CURRENT_USER, key_path)
            except FileNotFoundError:
                pass
                
        except Exception as e:
            print(f"注销文件处理器失败：{e}")
    
    def show_in_file_manager(self, file_path: str):
        """在 Windows 资源管理器中显示文件"""
        try:
            import subprocess
            subprocess.run(['explorer', '/select,', os.path.normpath(file_path)])
        except Exception:
            pass
    
    def set_taskbar_progress(self, progress: float):
        """设置 Windows 任务栏进度"""
        try:
            # 这里可以集成 Windows 任务栏 API
            # 需要使用 comtypes 或 pywin32
            pass
        except Exception:
            pass
    
    def enable_dark_titlebar(self, window):
        """启用 Windows 11 暗色标题栏"""
        try:
            import ctypes
            import ctypes.wintypes
            
            # Windows 11 暗色标题栏
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            value = ctypes.c_int(1)  # 启用暗色
            
            hwnd = ctypes.c_long(window.winfo_id())
            self.dwmapi.DwmSetWindowAttribute(
                hwnd,
                DWMWA_USE_IMMERSIVE_DARK_MODE,
                ctypes.byref(value),
                ctypes.sizeof(value)
            )
        except Exception:
            pass
    
    def get_system_theme(self) -> str:
        """获取 Windows 系统主题"""
        try:
            import winreg
            
            # 读取注册表获取系统主题
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
            
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
                apps_use_light, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
                
                if apps_use_light == 0:
                    return "dark"
                else:
                    return "light"
                    
        except Exception:
            return "dark"
    
    def optimize_for_touch(self):
        """优化触摸交互（针对 Windows 触摸屏设备）"""
        # 增加触摸目标大小
        pass
    
    def optimize_for_high_dpi(self):
        """优化 Windows 高 DPI 显示"""
        try:
            import ctypes
            
            # 声明 DPI 感知模式
            ctypes.windll.shcore.SetProcessDpiAwareness(2)  # Per-Monitor DPI Aware
        except Exception:
            try:
                # 旧版本 Windows
                ctypes.windll.user32.SetProcessDPIAware()
            except Exception:
                pass


class WindowsContextMenu:
    """Windows 右键菜单管理器"""
    
    @staticmethod
    def add_to_context_menu():
        """添加到右键菜单"""
        try:
            import winreg
            
            # 添加到所有文件的右键菜单
            key_path = r"Software\Classes\*\shell\MusicMeta"
            
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
                winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "编辑元数据 (&M)")
                winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, sys.executable)
            
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"{key_path}\\command") as key:
                script_path = os.path.abspath(__file__)
                while not os.path.exists(os.path.join(script_path, "main.py")):
                    script_path = os.path.dirname(script_path)
                
                main_py = os.path.join(script_path, "main.py")
                cmd = f'python "{main_py}" "%1"'
                winreg.SetValueEx(key, "", 0, winreg.REG_SZ, cmd)
                
            return True
            
        except Exception as e:
            print(f"添加右键菜单失败：{e}")
            return False
    
    @staticmethod
    def remove_from_context_menu():
        """从右键菜单移除"""
        try:
            import winreg
            
            key_path = r"Software\Classes\*\shell\MusicMeta"
            
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
                    winreg.DeleteKey(key, "command")
                winreg.DeleteKey(winreg.HKEY_CURRENT_USER, key_path)
                return True
            except FileNotFoundError:
                return False
                
        except Exception as e:
            print(f"移除右键菜单失败：{e}")
            return False
