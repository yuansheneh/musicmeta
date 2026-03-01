"""
GUI 组件库 - 可复用的 UI 组件
"""

import customtkinter as ctk
from tkinter import filedialog
from typing import Optional, Callable, Dict, Any
from PIL import Image, ImageTk
import io


class CoverArtViewer(ctk.CTkFrame):
    """封面艺术查看器"""
    
    COVER_SIZE = 300
    
    def __init__(self, parent, on_cover_change: Optional[Callable] = None):
        super().__init__(parent)
        
        self.on_cover_change = on_cover_change
        self.current_cover: Optional[Image.Image] = None
        
        self._create_ui()
    
    def _create_ui(self):
        """创建 UI"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # 封面显示区域
        self.cover_label = ctk.CTkLabel(
            self,
            text="🎵\n\n拖拽封面到此处\n或点击上传",
            font=ctk.CTkFont(size=16),
            compound="center",
            width=self.COVER_SIZE,
            height=self.COVER_SIZE,
            fg_color=self._get_color("bg_card"),
            corner_radius=10,
        )
        self.cover_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # 绑定点击事件
        self.cover_label.bind("<Button-1>", lambda e: self._upload_cover())
        
        # 按钮组
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.grid(row=1, column=0, pady=10)
        
        self.upload_btn = ctk.CTkButton(
            self.btn_frame,
            text="上传封面",
            command=self._upload_cover,
            width=100,
        )
        self.upload_btn.pack(side="left", padx=5)
        
        self.remove_btn = ctk.CTkButton(
            self.btn_frame,
            text="移除封面",
            command=self._remove_cover,
            width=100,
            fg_color="transparent",
            border_width=1,
        )
        self.remove_btn.pack(side="left", padx=5)
    
    def _get_color(self, name: str) -> str:
        """获取颜色"""
        from .theme_manager import ThemeManager
        tm = ThemeManager()
        return tm.get_color(name)
    
    def _upload_cover(self):
        """上传封面"""
        filetypes = [
            ("图片文件", "*.png *.jpg *.jpeg *.webp"),
            ("PNG 文件", "*.png"),
            ("JPEG 文件", "*.jpg *.jpeg"),
        ]
        
        file_path = filedialog.askopenfilename(
            title="选择封面图片",
            filetypes=filetypes
        )
        
        if file_path:
            try:
                image = Image.open(file_path)
                # 转换为正方形并调整大小
                image = self._crop_to_square(image)
                image = image.resize((self.COVER_SIZE, self.COVER_SIZE), Image.Resampling.LANCZOS)
                
                self.set_cover(image)
                
                if self.on_change:
                    self.on_change(image)
                
            except Exception as e:
                print(f"加载封面失败：{e}")
    
    def _crop_to_square(self, image: Image.Image) -> Image.Image:
        """裁剪为正方形"""
        width, height = image.size
        min_dim = min(width, height)
        
        left = (width - min_dim) // 2
        top = (height - min_dim) // 2
        right = left + min_dim
        bottom = top + min_dim
        
        return image.crop((left, top, right, bottom))
    
    def _remove_cover(self):
        """移除封面"""
        self.clear_cover()
        
        if self.on_cover_change:
            self.on_cover_change(None)
    
    def set_cover(self, image: Image.Image):
        """设置封面"""
        self.current_cover = image
        
        # 转换为 PhotoImage
        photo = ImageTk.PhotoImage(image)
        
        # 更新标签
        self.cover_label.configure(
            image=photo,
            text="",
            compound="center"
        )
        self.cover_label.image = photo  # 保持引用
    
    def clear_cover(self):
        """清除封面"""
        self.current_cover = None
        
        self.cover_label.configure(
            image="",
            text="🎵\n\n拖拽封面到此处\n或点击上传",
            font=ctk.CTkFont(size=16),
        )


class MetadataEditor(ctk.CTkScrollableFrame):
    """元数据编辑器"""
    
    def __init__(self, parent, on_change: Optional[Callable] = None):
        super().__init__(parent)
        
        self.on_change = on_change
        self.current_metadata = None
        
        # 存储输入控件
        self.entries: Dict[str, Any] = {}
        
        self._create_ui()
    
    def _create_ui(self):
        """创建 UI"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        row = 0
        
        # 基本信息
        self._create_section_header("基本信息", row)
        row += 1
        
        self._create_entry_pair("标题", "artist", "艺术家", row, "title")
        row += 1
        
        self._create_entry_pair("专辑", "album_artist", "专辑艺术家", row, "album")
        row += 1
        
        # 编号信息
        self._create_section_header("编号信息", row)
        row += 1
        
        self._create_entry_pair("年份", "track_number", "曲目编号", row, "year")
        row += 1
        
        self._create_entry_pair("光盘编号", "disc_total", "总光盘数", row, "disc_number")
        row += 1
        
        # 分类信息
        self._create_section_header("分类信息", row)
        row += 1
        
        self._create_entry_full("流派", "genre", row)
        row += 1
        
        self._create_entry_full("注释", "comment", row)
        row += 1
        
        # 高级信息
        self._create_section_header("高级信息", row)
        row += 1
        
        self._create_entry_pair("作曲家", "conductor", "指挥家", row, "composer")
        row += 1
        
        self._create_entry_pair("混音师", "publisher", "出版商", row, "remixer")
        row += 1
        
        self._create_entry_full("版权", "copyright", row)
        row += 1
        
        self._create_entry_full("编码者", "encoded_by", row)
        row += 1
        
        # 媒体信息
        self._create_section_header("媒体信息", row)
        row += 1
        
        self._create_entry_pair("BPM", "mood", "情绪", row, "bpm")
        row += 1
        
        self._create_entry_full("歌词", "lyrics", row, is_multiline=True)
        row += 1
        
        # 技术信息（只读）
        self._create_section_header("技术信息", row)
        row += 1
        
        self._create_readonly_pair("时长", "duration", "比特率", row, "bitrate")
        row += 1
        
        self._create_readonly_pair("采样率", "sample_rate", "声道数", row, "channels")
        row += 1
        
        self._create_readonly_full("编解码器", "codec", row)
        row += 1
        
        self._create_readonly_full("标签类型", "tags_type", row)
        row += 2
        
        # 文件信息
        self._create_section_header("文件信息", row)
        row += 1
        
        self._create_readonly_full("文件路径", "file_path", row)
        row += 1
        
        self._create_readonly_pair("文件大小", "file_size", "创建时间", row, "file_created")
    
    def _create_section_header(self, text: str, row: int):
        """创建分组标题"""
        header = ctk.CTkLabel(
            self,
            text=text,
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        header.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(15, 5), padx=5)
    
    def _create_entry_pair(self, label1: str, key1: str, label2: str, row: int, key2: str):
        """创建一对输入框"""
        # 第一个字段
        ctk.CTkLabel(self, text=label1, anchor="w").grid(
            row=row, column=0, sticky="ew", padx=5, pady=2
        )
        entry1 = ctk.CTkEntry(self)
        entry1.grid(row=row+1, column=0, sticky="ew", padx=5, pady=2)
        entry1.bind("<KeyRelease>", lambda e: self._on_change())
        self.entries[key1] = entry1
        
        # 第二个字段
        ctk.CTkLabel(self, text=label2, anchor="w").grid(
            row=row, column=1, sticky="ew", padx=5, pady=2
        )
        entry2 = ctk.CTkEntry(self)
        entry2.grid(row=row+1, column=1, sticky="ew", padx=5, pady=2)
        entry2.bind("<KeyRelease>", lambda e: self._on_change())
        self.entries[key2] = entry2
    
    def _create_entry_full(self, label: str, key: str, row: int, is_multiline: bool = False):
        """创建全宽输入框"""
        ctk.CTkLabel(self, text=label, anchor="w").grid(
            row=row, column=0, columnspan=2, sticky="ew", padx=5, pady=2
        )
        
        if is_multiline:
            entry = ctk.CTkTextbox(self, height=100)
        else:
            entry = ctk.CTkEntry(self)
        
        entry.grid(row=row+1, column=0, columnspan=2, sticky="ew", padx=5, pady=2)
        entry.bind("<KeyRelease>", lambda e: self._on_change())
        self.entries[key] = entry
    
    def _create_readonly_pair(self, label1: str, key1: str, label2: str, row: int, key2: str):
        """创建一对只读字段"""
        # 第一个字段
        ctk.CTkLabel(self, text=label1, anchor="w").grid(
            row=row, column=0, sticky="ew", padx=5, pady=2
        )
        entry1 = ctk.CTkEntry(self, state="disabled")
        entry1.grid(row=row+1, column=0, sticky="ew", padx=5, pady=2)
        self.entries[key1] = entry1
        
        # 第二个字段
        ctk.CTkLabel(self, text=label2, anchor="w").grid(
            row=row, column=1, sticky="ew", padx=5, pady=2
        )
        entry2 = ctk.CTkEntry(self, state="disabled")
        entry2.grid(row=row+1, column=1, sticky="ew", padx=5, pady=2)
        self.entries[key2] = entry2
    
    def _create_readonly_full(self, label: str, key: str, row: int):
        """创建全宽只读字段"""
        ctk.CTkLabel(self, text=label, anchor="w").grid(
            row=row, column=0, columnspan=2, sticky="ew", padx=5, pady=2
        )
        entry = ctk.CTkEntry(self, state="disabled")
        entry.grid(row=row+1, column=0, columnspan=2, sticky="ew", padx=5, pady=2)
        self.entries[key] = entry
    
    def _on_change(self):
        """内容变更回调"""
        if self.on_change:
            self.on_change()
    
    def load_metadata(self, metadata):
        """加载元数据"""
        self.current_metadata = metadata
        
        # 基本信息
        self._set_entry("title", metadata.title)
        self._set_entry("artist", metadata.artist)
        self._set_entry("album", metadata.album)
        self._set_entry("album_artist", metadata.album_artist)
        
        # 编号信息
        self._set_entry("year", str(metadata.year) if metadata.year else "")
        self._set_entry("track_number", str(metadata.track_number) if metadata.track_number else "")
        self._set_entry("disc_number", str(metadata.disc_number) if metadata.disc_number else "")
        self._set_entry("disc_total", str(metadata.disc_total) if metadata.disc_total else "")
        
        # 分类信息
        self._set_entry("genre", metadata.genre)
        self._set_entry("comment", metadata.comment)
        
        # 高级信息
        self._set_entry("composer", metadata.composer)
        self._set_entry("conductor", metadata.conductor)
        self._set_entry("remixer", metadata.remixer)
        self._set_entry("publisher", metadata.publisher)
        self._set_entry("copyright", metadata.copyright)
        self._set_entry("encoded_by", metadata.encoded_by)
        
        # 媒体信息
        self._set_entry("bpm", str(metadata.bpm) if metadata.bpm else "")
        self._set_entry("mood", metadata.mood)
        self._set_entry("lyrics", metadata.lyrics)
        
        # 技术信息
        if metadata.duration:
            mins = int(metadata.duration // 60)
            secs = int(metadata.duration % 60)
            self._set_entry("duration", f"{mins}:{secs:02d}")
        
        self._set_entry("bitrate", f"{metadata.bit_rate // 1000} kbps" if metadata.bit_rate else "")
        self._set_entry("sample_rate", f"{metadata.sample_rate} Hz" if metadata.sample_rate else "")
        self._set_entry("channels", str(metadata.channels) if metadata.channels else "")
        self._set_entry("codec", metadata.codec)
        self._set_entry("tags_type", metadata.tags_type)
        
        # 文件信息
        self._set_entry("file_path", metadata.file_path)
        self._set_entry("file_size", self._format_size(metadata.file_size) if metadata.file_size else "")
    
    def save_metadata(self, metadata):
        """保存元数据到对象"""
        # 基本信息
        metadata.title = self._get_entry_text("title")
        metadata.artist = self._get_entry_text("artist")
        metadata.album = self._get_entry_text("album")
        metadata.album_artist = self._get_entry_text("album_artist")
        
        # 编号信息
        metadata.year = self._get_int("year")
        metadata.track_number = self._get_int("track_number")
        metadata.disc_number = self._get_int("disc_number")
        metadata.disc_total = self._get_int("disc_total")
        
        # 分类信息
        metadata.genre = self._get_entry_text("genre")
        metadata.comment = self._get_entry_text("comment")
        
        # 高级信息
        metadata.composer = self._get_entry_text("composer")
        metadata.conductor = self._get_entry_text("conductor")
        metadata.remixer = self._get_entry_text("remixer")
        metadata.publisher = self._get_entry_text("publisher")
        metadata.copyright = self._get_entry_text("copyright")
        metadata.encoded_by = self._get_entry_text("encoded_by")
        
        # 媒体信息
        metadata.bpm = self._get_float("bpm")
        metadata.mood = self._get_entry_text("mood")
        metadata.lyrics = self._get_entry_text("lyrics")
    
    def _set_entry(self, key: str, value: str):
        """设置输入框值"""
        if key in self.entries:
            entry = self.entries[key]
            entry.delete(0, 'end')
            entry.insert(0, value or "")
    
    def _get_entry_text(self, key: str) -> Optional[str]:
        """获取输入框文本"""
        if key in self.entries:
            entry = self.entries[key]
            text = entry.get().strip()
            return text if text else None
        return None
    
    def _get_int(self, key: str) -> Optional[int]:
        """获取整数值"""
        text = self._get_entry_text(key)
        if text:
            try:
                return int(text)
            except ValueError:
                pass
        return None
    
    def _get_float(self, key: str) -> Optional[float]:
        """获取浮点数值"""
        text = self._get_entry_text(key)
        if text:
            try:
                return float(text)
            except ValueError:
                pass
        return None
    
    def _format_size(self, size: int) -> str:
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"


class FileListPanel(ctk.CTkFrame):
    """文件列表面板"""
    
    def __init__(self, parent, on_file_select: Optional[Callable] = None):
        super().__init__(parent)
        
        self.on_file_select = on_file_select
        
        self._create_ui()
    
    def _create_ui(self):
        """创建 UI"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # 标题
        self.title_label = ctk.CTkLabel(
            self,
            text="文件列表",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        self.title_label.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        
        # 搜索框
        self.search_entry = ctk.CTkEntry(self, placeholder_text="搜索文件...")
        self.search_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.search_entry.bind("<KeyRelease>", lambda e: self._filter_files())
        
        # 文件列表
        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)
        
        self.file_buttons = []
    
    def load_files(self, files: list):
        """加载文件列表"""
        # 清空现有按钮
        for btn in self.file_buttons:
            btn.destroy()
        self.file_buttons = []
        
        # 创建文件按钮
        for file_path in files:
            btn = ctk.CTkButton(
                self.scroll_frame,
                text=os.path.basename(file_path),
                command=lambda p=file_path: self._on_select(p),
                anchor="w",
                height=35,
            )
            btn.pack(fill="x", pady=2)
            self.file_buttons.append((btn, file_path))
    
    def _on_select(self, file_path: str):
        """文件选择回调"""
        if self.on_file_select:
            self.on_file_select(file_path)
    
    def _filter_files(self):
        """过滤文件"""
        search_text = self.search_entry.get().lower()
        
        for btn, file_path in self.file_buttons:
            if search_text in os.path.basename(file_path).lower():
                btn.pack(fill="x", pady=2)
            else:
                btn.pack_forget()


class StatusBar(ctk.CTkFrame):
    """状态栏"""
    
    def __init__(self, parent):
        super().__init__(parent, height=30)
        
        self.grid_columnconfigure(0, weight=1)
        
        # 状态标签
        self.status_label = ctk.CTkLabel(
            self,
            text="就绪",
            anchor="w",
            font=ctk.CTkFont(size=11)
        )
        self.status_label.grid(row=0, column=0, sticky="ew", padx=10)
        
        # 进度条（隐藏）
        self.progress_bar = ctk.CTkProgressBar(self, width=200)
        self.progress_bar.grid(row=0, column=1, padx=10)
        self.progress_bar.grid_remove()
    
    def show_status(self, message: str, color: str = "default"):
        """显示状态消息"""
        self.status_label.configure(text=message)
    
    def show_loading(self, message: str = "加载中..."):
        """显示加载状态"""
        self.status_label.configure(text=message)
        self.progress_bar.grid()
        self.progress_bar.start()
    
    def show_success(self, message: str):
        """显示成功消息"""
        self.status_label.configure(text=f"✓ {message}", text_color="#9ece6a")
        self.progress_bar.grid_remove()
        self.progress_bar.stop()
    
    def show_error(self, message: str):
        """显示错误消息"""
        self.status_label.configure(text=f"✗ {message}", text_color="#f7768e")
        self.progress_bar.grid_remove()
        self.progress_bar.stop()
    
    def show_warning(self, message: str):
        """显示警告消息"""
        self.status_label.configure(text=f"⚠ {message}", text_color="#e0af68")
        self.progress_bar.grid_remove()
        self.progress_bar.stop()
