"""
主窗口 - 应用的主要 GUI 界面
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
from typing import Optional, List, Dict
from PIL import Image, ImageTk
import io
import os
from pathlib import Path

from ..core.audio_loader import AudioLoader
from ..core.metadata import AudioMetadata, MetadataField
from .theme_manager import ThemeManager
from .components import MetadataEditor, FileListPanel, CoverArtViewer, StatusBar


class MainWindow(ctk.CTk):
    """主窗口类"""
    
    def __init__(self):
        super().__init__()
        
        # 初始化
        self.theme_manager = ThemeManager()
        self.audio_loader = AudioLoader()
        self.current_file: Optional[str] = None
        self.current_metadata: Optional[AudioMetadata] = None
        self.file_list: List[str] = []
        
        # 窗口配置
        self.title("MusicMeta - 音乐元数据编辑器")
        self.geometry("1400x900")
        self.minsize(1200, 700)
        
        # 应用主题
        self.theme_manager.apply_theme('dark')
        
        # 创建 UI
        self._create_ui()
        
        # 加载最近的文件
        self._load_recent_files()
    
    def _create_ui(self):
        """创建用户界面"""
        # 配置网格
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # 创建侧边栏
        self._create_sidebar()
        
        # 创建主内容区
        self._create_main_area()
        
        # 创建状态栏
        self._create_status_bar()
    
    def _create_sidebar(self):
        """创建侧边栏"""
        colors = self.theme_manager.current_colors
        
        self.sidebar_frame = ctk.CTkFrame(
            self,
            width=250,
            corner_radius=0,
            fg_color=colors['bg_card']
        )
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(1, weight=1)
        
        # Logo/标题
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="🎵 MusicMeta",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=colors['primary']
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # 操作按钮组
        self.btn_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.btn_frame.grid(row=1, column=0, padx=15, pady=10, sticky="n")
        
        # 打开文件按钮
        self.open_btn = ctk.CTkButton(
            self.btn_frame,
            text="📁 打开文件",
            command=self._open_file,
            height=45,
            font=ctk.CTkFont(size=14),
        )
        self.open_btn.pack(fill="x", pady=5)
        
        # 打开文件夹按钮
        self.open_folder_btn = ctk.CTkButton(
            self.btn_frame,
            text="📂 打开文件夹",
            command=self._open_folder,
            height=45,
            font=ctk.CTkFont(size=14),
        )
        self.open_folder_btn.pack(fill="x", pady=5)
        
        # 保存按钮
        self.save_btn = ctk.CTkButton(
            self.btn_frame,
            text="💾 保存",
            command=self._save_metadata,
            height=45,
            font=ctk.CTkFont(size=14),
            state="disabled"
        )
        self.save_btn.pack(fill="x", pady=5)
        
        # 另存为按钮
        self.save_as_btn = ctk.CTkButton(
            self.btn_frame,
            text="💾 另存为",
            command=self._save_as,
            height=45,
            font=ctk.CTkFont(size=14),
            state="disabled"
        )
        self.save_as_btn.pack(fill="x", pady=5)
        
        # 批量编辑按钮
        self.batch_btn = ctk.CTkButton(
            self.btn_frame,
            text="📝 批量编辑",
            command=self._open_batch_editor,
            height=45,
            font=ctk.CTkFont(size=14),
        )
        self.batch_btn.pack(fill="x", pady=5)
        
        # 主题选择
        self.theme_label = ctk.CTkLabel(
            self.btn_frame,
            text="主题:",
            font=ctk.CTkFont(size=12),
        )
        self.theme_label.pack(pady=(20, 5))
        
        self.theme_var = ctk.StringVar(value="dark")
        self.theme_menu = ctk.CTkOptionMenu(
            self.btn_frame,
            variable=self.theme_var,
            values=list(self.theme_manager.get_all_themes().keys()),
            command=self._change_theme,
            width=200,
        )
        self.theme_menu.pack(pady=5)
        
        # 最近文件
        self.recent_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="最近文件",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=colors['text_primary']
        )
        self.recent_label.grid(row=2, column=0, padx=15, pady=(10, 5), sticky="w")
        
        self.recent_listbox = ctk.CTkScrollableFrame(
            self.sidebar_frame,
            fg_color="transparent"
        )
        self.recent_listbox.grid(row=3, column=0, padx=15, pady=5, sticky="nsew")
    
    def _create_main_area(self):
        """创建主内容区"""
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        # 配置网格
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # 文件路径显示
        self._create_file_info_bar()
        
        # 创建内容区（左右分栏）
        self._create_content_area()
    
    def _create_file_info_bar(self):
        """创建文件信息栏"""
        self.file_info_frame = ctk.CTkFrame(self.main_frame)
        self.file_info_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        self.file_path_label = ctk.CTkLabel(
            self.file_info_frame,
            text="未选择文件",
            font=ctk.CTkFont(size=12),
            anchor="w"
        )
        self.file_path_label.pack(side="left", fill="x", expand=True, padx=10, pady=10)
        
        self.file_format_label = ctk.CTkLabel(
            self.file_info_frame,
            text="",
            font=ctk.CTkFont(size=11),
            text_color=self.theme_manager.current_colors['text_secondary']
        )
        self.file_format_label.pack(side="right", padx=10)
    
    def _create_content_area(self):
        """创建内容区"""
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.grid(row=1, column=0, sticky="nsew")
        
        # 配置网格
        self.content_frame.grid_columnconfigure(1, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
        
        # 左侧：封面艺术
        self._create_cover_panel()
        
        # 右侧：元数据编辑器
        self._create_editor_panel()
    
    def _create_cover_panel(self):
        """创建封面面板"""
        self.cover_frame = ctk.CTkFrame(self.content_frame, width=350)
        self.cover_frame.grid(row=0, column=0, sticky="ns", padx=(0, 10))
        self.cover_frame.grid_propagate(False)
        
        self.cover_viewer = CoverArtViewer(
            self.cover_frame,
            on_cover_change=self._on_cover_change
        )
        self.cover_viewer.pack(fill="both", expand=True, padx=10, pady=10)
    
    def _create_editor_panel(self):
        """创建编辑器面板"""
        self.editor_frame = ctk.CTkScrollableFrame(self.content_frame)
        self.editor_frame.grid(row=0, column=1, sticky="nsew")
        
        self.metadata_editor = MetadataEditor(
            self.editor_frame,
            on_change=self._on_metadata_change
        )
        self.metadata_editor.pack(fill="both", expand=True, padx=10, pady=10)
    
    def _create_status_bar(self):
        """创建状态栏"""
        self.status_bar = StatusBar(self)
        self.status_bar.grid(row=1, column=0, columnspan=2, sticky="ew")
    
    def _open_file(self):
        """打开文件"""
        filetypes = [
            ("音频文件", "*.mp3 *.flac *.ogg *.m4a *.wma *.wav *.aiff *.ape"),
            ("MP3 文件", "*.mp3"),
            ("FLAC 文件", "*.flac"),
            ("OGG 文件", "*.ogg *.oga"),
            ("M4A/AAC 文件", "*.m4a *.aac"),
            ("WMA 文件", "*.wma"),
            ("所有文件", "*.*")
        ]
        
        file_path = filedialog.askopenfilename(
            title="选择音频文件",
            filetypes=filetypes
        )
        
        if file_path:
            self._load_file(file_path)
    
    def _open_folder(self):
        """打开文件夹"""
        folder_path = filedialog.askdirectory(title="选择音乐文件夹")
        
        if folder_path:
            self._load_folder(folder_path)
    
    def _load_file(self, file_path: str):
        """加载文件"""
        try:
            self.status_bar.show_loading("正在加载文件...")
            
            # 加载元数据
            self.current_metadata = self.audio_loader.load(file_path)
            self.current_file = file_path
            
            # 更新 UI
            self._update_ui_for_file()
            
            self.status_bar.show_success(f"已加载：{os.path.basename(file_path)}")
            
        except Exception as e:
            self.status_bar.show_error(f"加载失败：{str(e)}")
            messagebox.showerror("错误", f"无法加载文件:\n{str(e)}")
    
    def _load_folder(self, folder_path: str):
        """加载文件夹"""
        try:
            self.status_bar.show_loading("正在扫描文件夹...")
            
            # 扫描音频文件
            supported_exts = AudioLoader.get_supported_formats().keys()
            self.file_list = []
            
            for ext in supported_exts:
                self.file_list.extend(Path(folder_path).rglob(f"*{ext}"))
            
            self.file_list = [str(f) for f in self.file_list]
            
            if self.file_list:
                # 加载第一个文件
                self._load_file(self.file_list[0])
                self.status_bar.show_success(f"找到 {len(self.file_list)} 个音频文件")
            else:
                self.status_bar.show_warning("未找到音频文件")
            
        except Exception as e:
            self.status_bar.show_error(f"扫描失败：{str(e)}")
    
    def _update_ui_for_file(self):
        """更新 UI 显示当前文件"""
        if not self.current_metadata:
            return
        
        # 更新文件路径显示
        self.file_path_label.configure(text=self.current_file)
        
        # 更新格式显示
        format_text = f"{self.current_metadata.codec or 'Unknown'} | "
        if self.current_metadata.duration:
            mins = int(self.current_metadata.duration // 60)
            secs = int(self.current_metadata.duration % 60)
            format_text += f"{mins}:{secs:02d} | "
        if self.current_metadata.bit_rate:
            format_text += f"{self.current_metadata.bit_rate // 1000}kbps"
        
        self.file_format_label.configure(text=format_text)
        
        # 更新封面
        if self.current_metadata.has_cover():
            self.cover_viewer.set_cover(self.current_metadata.cover_art)
        else:
            self.cover_viewer.clear_cover()
        
        # 更新元数据编辑器
        self.metadata_editor.load_metadata(self.current_metadata)
        
        # 启用保存按钮
        self.save_btn.configure(state="normal")
        self.save_as_btn.configure(state="normal")
    
    def _save_metadata(self):
        """保存元数据"""
        if not self.current_file or not self.current_metadata:
            return
        
        try:
            self.status_bar.show_loading("正在保存...")
            
            # 从编辑器获取更新的数据
            self.metadata_editor.save_metadata(self.current_metadata)
            
            # 保存到文件
            self.audio_loader.save(self.current_metadata)
            
            self.status_bar.show_success("保存成功!")
            
        except Exception as e:
            self.status_bar.show_error(f"保存失败：{str(e)}")
            messagebox.showerror("错误", f"无法保存元数据:\n{str(e)}")
    
    def _save_as(self):
        """另存为"""
        if not self.current_metadata:
            return
        
        filetypes = [
            ("MP3 文件", "*.mp3"),
            ("FLAC 文件", "*.flac"),
            ("OGG 文件", "*.ogg"),
            ("M4A 文件", "*.m4a"),
            ("所有文件", "*.*")
        ]
        
        file_path = filedialog.asksaveasfilename(
            title="另存为",
            filetypes=filetypes,
            defaultextension=".mp3"
        )
        
        if file_path:
            try:
                self.status_bar.show_loading("正在保存...")
                
                # 从编辑器获取更新的数据
                self.metadata_editor.save_metadata(self.current_metadata)
                
                # 保存到新文件
                self.audio_loader.save(self.current_metadata, file_path)
                
                # 更新当前文件
                self._load_file(file_path)
                
                self.status_bar.show_success(f"已保存到：{file_path}")
                
            except Exception as e:
                self.status_bar.show_error(f"保存失败：{str(e)}")
    
    def _on_cover_change(self, cover_image: Optional[Image.Image]):
        """封面变更回调"""
        if self.current_metadata:
            self.current_metadata.cover_art = cover_image
            if cover_image:
                self.current_metadata.cover_art_mime = 'image/jpeg'
    
    def _on_metadata_change(self):
        """元数据变更回调"""
        # 标记为已修改
        if not self.save_btn.cget("text").startswith("●"):
            self.save_btn.configure(text="● 保存")
    
    def _change_theme(self, theme_name: str):
        """切换主题"""
        self.theme_manager.apply_theme(theme_name)
        # 重新加载 UI 样式
        self._update_ui_style()
    
    def _update_ui_style(self):
        """更新 UI 样式"""
        colors = self.theme_manager.current_colors
        
        # 更新侧边栏颜色
        self.sidebar_frame.configure(fg_color=colors['bg_card'])
        
        # 更新其他组件颜色
        # ... (根据需要更新更多组件)
    
    def _open_batch_editor(self):
        """打开批量编辑器"""
        # TODO: 实现批量编辑器窗口
        messagebox.showinfo("提示", "批量编辑功能开发中...")
    
    def _load_recent_files(self):
        """加载最近文件列表"""
        # TODO: 从配置文件加载最近文件
        pass
    
    def _add_to_recent(self, file_path: str):
        """添加到最近文件列表"""
        # TODO: 保存到配置文件
        pass
    
    def on_closing(self):
        """窗口关闭处理"""
        # TODO: 保存未保存的更改
        self.destroy()


def main():
    """主函数"""
    app = MainWindow()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()


if __name__ == "__main__":
    main()
