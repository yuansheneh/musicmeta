"""
主题管理器 - 管理应用主题和样式
"""

import customtkinter as ctk
from typing import Dict, Any
import json
import os
from pathlib import Path


class ThemeManager:
    """主题管理器"""
    
    # 内置主题
    THEMES = {
        "dark": {
            "name": "暗黑模式",
            "ctk_theme": "dark",
            "colors": {
                "primary": "#8B5CF6",
                "secondary": "#EC4899",
                "accent": "#10B981",
                "bg_main": "#1a1b26",
                "bg_card": "#24283b",
                "bg_hover": "#2f3549",
                "text_primary": "#a9b1d6",
                "text_secondary": "#565f89",
                "border": "#414868",
                "success": "#9ece6a",
                "warning": "#e0af68",
                "error": "#f7768e",
            }
        },
        "light": {
            "name": "明亮模式",
            "ctk_theme": "light",
            "colors": {
                "primary": "#7C3AED",
                "secondary": "#EC4899",
                "accent": "#059669",
                "bg_main": "#ffffff",
                "bg_card": "#f9fafb",
                "bg_hover": "#f3f4f6",
                "text_primary": "#1f2937",
                "text_secondary": "#6b7280",
                "border": "#e5e7eb",
                "success": "#059669",
                "warning": "#d97706",
                "error": "#dc2626",
            }
        },
        "ocean": {
            "name": "海洋",
            "ctk_theme": "dark",
            "colors": {
                "primary": "#0077b6",
                "secondary": "#00b4d8",
                "accent": "#90e0ef",
                "bg_main": "#03045e",
                "bg_card": "#0077b6",
                "bg_hover": "#0096c7",
                "text_primary": "#caf0f8",
                "text_secondary": "#48cae4",
                "border": "#023e8a",
                "success": "#00ff88",
                "warning": "#ffd60a",
                "error": "#ff6b6b",
            }
        },
        "sunset": {
            "name": "日落",
            "ctk_theme": "dark",
            "colors": {
                "primary": "#ff6b6b",
                "secondary": "#feca57",
                "accent": "#ff9ff3",
                "bg_main": "#2c2c54",
                "bg_card": "#474787",
                "bg_hover": "#68689e",
                "text_primary": "#f5f6fa",
                "text_secondary": "#dcdde1",
                "border": "#778beb",
                "success": "#78e08f",
                "warning": "#f9ca24",
                "error": "#eb4d4b",
            }
        },
        "forest": {
            "name": "森林",
            "ctk_theme": "dark",
            "colors": {
                "primary": "#2d6a4f",
                "secondary": "#52b788",
                "accent": "#95d5b2",
                "bg_main": "#1b4332",
                "bg_card": "#2d6a4f",
                "bg_hover": "#40916c",
                "text_primary": "#d8f3dc",
                "text_secondary": "#b7e4c7",
                "border": "#74c69d",
                "success": "#95d5b2",
                "warning": "#d4e09b",
                "error": "#e63946",
            }
        },
    }
    
    def __init__(self):
        self.current_theme = "dark"
        self.config_dir = Path.home() / ".musicmeta"
        self.config_file = self.config_dir / "theme_config.json"
        self._load_config()
    
    def _load_config(self):
        """加载用户配置"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.current_theme = config.get('theme', 'dark')
            except Exception:
                pass
    
    def _save_config(self):
        """保存用户配置"""
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump({'theme': self.current_theme}, f, indent=2)
        except (PermissionError, OSError):
            # 如果无法写入用户目录，使用临时目录
            import tempfile
            temp_dir = Path(tempfile.gettempdir()) / "musicmeta"
            temp_dir.mkdir(parents=True, exist_ok=True)
            self.config_file = temp_dir / "theme_config.json"
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump({'theme': self.current_theme}, f, indent=2)
    
    def apply_theme(self, theme_name: str):
        """应用主题"""
        if theme_name not in self.THEMES:
            theme_name = 'dark'
        
        self.current_theme = theme_name
        theme = self.THEMES[theme_name]
        
        # 设置 CustomTkinter 主题
        ctk.set_appearance_mode(theme['ctk_theme'])
        
        # 设置颜色主题
        ctk.set_default_color_theme("blue")
        
        self._save_config()
    
    def get_theme(self, theme_name: str = None) -> Dict[str, Any]:
        """获取主题配置"""
        theme_name = theme_name or self.current_theme
        return self.THEMES.get(theme_name, self.THEMES['dark'])
    
    def get_color(self, color_name: str, theme_name: str = None) -> str:
        """获取主题颜色"""
        theme = self.get_theme(theme_name)
        return theme['colors'].get(color_name, '#8B5CF6')
    
    def get_all_themes(self) -> Dict[str, str]:
        """获取所有主题名称"""
        return {k: v['name'] for k, v in self.THEMES.items()}
    
    def configure_widget(self, widget, widget_type: str = "default"):
        """配置组件样式"""
        theme = self.get_theme()
        colors = theme['colors']
        
        if widget_type == "button_primary":
            widget.configure(
                fg_color=colors['primary'],
                hover_color=self._adjust_brightness(colors['primary'], 20),
                border_color=colors['border'],
            )
        elif widget_type == "button_secondary":
            widget.configure(
                fg_color=colors['secondary'],
                hover_color=self._adjust_brightness(colors['secondary'], 20),
            )
        elif widget_type == "frame_card":
            widget.configure(
                fg_color=colors['bg_card'],
                border_color=colors['border'],
                border_width=1,
            )
        elif widget_type == "entry":
            widget.configure(
                fg_color=colors['bg_main'],
                border_color=colors['border'],
            )
    
    def _adjust_brightness(self, hex_color: str, amount: int) -> str:
        """调整颜色亮度"""
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        
        r = max(0, min(255, r + amount))
        g = max(0, min(255, g + amount))
        b = max(0, min(255, b + amount))
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    @property
    def current_colors(self) -> Dict[str, str]:
        """获取当前主题颜色"""
        return self.get_theme()['colors']
