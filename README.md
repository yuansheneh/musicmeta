# 🎵 MusicMeta - 跨平台音乐元数据编辑器

一个功能强大、界面华丽的跨平台音乐元数据编辑工具，专为 Windows 和 Android 优化，同时支持 macOS 和 Linux。

![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Android%20%7C%20macOS%20%7C%20Linux-blue)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ 主要特性

### 🎨 华丽的 GUI 界面
- **多主题支持**: 内置暗黑、明亮、海洋、日落、森林 5 种精美主题
- **实时预览**: 封面艺术和元数据实时显示
- **现代化设计**: 基于 CustomTkinter 的流畅界面
- **高 DPI 适配**: 完美支持 4K 和高分辨率屏幕

### 📀 多种音频格式支持
- **MP3** - ID3v1, ID3v2.3, ID3v2.4
- **FLAC** - Vorbis Comments
- **OGG Vorbis/Opus** - Vorbis Comments
- **M4A/AAC** - iTunes MP4 标签
- **WMA** - ASF 标签
- **WAV** - INFO chunk
- **AIFF** - ID3 标签
- **APE** - APEv2 标签

### 🖥️ Windows 特殊优化
- ✅ 文件资源管理器集成
- ✅ 右键菜单快速访问
- ✅ 任务栏进度显示
- ✅ Windows 11 暗色标题栏
- ✅ 高 DPI 自动缩放
- ✅ 系统主题自动检测

### 📱 Android 特殊优化
- ✅ Material You 动态取色
- ✅ 存储访问框架 (SAF)
- ✅ 后台元数据扫描
- ✅ 触摸优化界面
- ✅ 移动网络优化
- ✅ 媒体扫描器集成

### 🛠️ 强大的编辑功能
- **基本元数据**: 标题、艺术家、专辑、年份等
- **高级元数据**: 作曲家、指挥家、混音师、出版商等
- **媒体信息**: BPM、情绪、歌词、评级
- **封面艺术**: 上传、查看、移除专辑封面
- **批量编辑**: 同时处理多个文件
- **查找替换**: 快速批量修改元数据
- **从文件名标记**: 自动从文件名提取信息

## 🚀 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行应用

**Windows:**
```batch
run.bat
```

**Linux/macOS:**
```bash
chmod +x run.sh
./run.sh
```

**直接运行:**
```bash
python run.py
```

### 命令行模式

```bash
# 显示文件信息
python run.py song.mp3 --info

# 启动 GUI
python run.py --gui
```

## 📖 使用指南

### 基本使用

1. **打开文件**: 点击"📁 打开文件"按钮选择音频文件
2. **编辑元数据**: 在右侧编辑器中修改元数据字段
3. **更换封面**: 点击封面区域上传新封面图片
4. **保存**: 点击"💾 保存"按钮保存更改

### 批量编辑

1. 点击"📂 打开文件夹"加载整个音乐库
2. 选择多个文件
3. 使用批量编辑功能统一修改元数据
4. 支持查找替换、复制元数据等操作

### 主题切换

在左侧边栏的主题下拉菜单中选择喜欢的主题：
- 🌑 暗黑模式 - 护眼舒适
- ☀️ 明亮模式 - 清晰明快
- 🌊 海洋 - 深邃蓝色
- 🌅 日落 - 温暖橙色
- 🌲 森林 - 自然绿色

## 📁 项目结构

```
musicmeta/
├── src/
│   ├── core/              # 核心元数据处理引擎
│   │   ├── metadata.py    # 元数据模型
│   │   ├── audio_loader.py # 音频加载器
│   │   └── tag_mapper.py  # 标签映射器
│   ├── gui/               # 图形用户界面
│   │   ├── main_window.py # 主窗口
│   │   ├── components.py  # UI 组件
│   │   └── theme_manager.py # 主题管理器
│   ├── platforms/         # 平台特定优化
│   │   ├── windows_optimizer.py
│   │   ├── android_optimizer.py
│   │   └── base_optimizer.py
│   ├── utils/             # 工具函数
│   │   └── batch_editor.py # 批量编辑器
│   └── main.py            # 程序入口
├── assets/                # 资源文件
├── tests/                 # 测试文件
├── requirements.txt       # Python 依赖
├── pyproject.toml         # 项目配置
└── README.md             # 说明文档
```

## 🔧 开发

### 安装开发依赖

```bash
pip install -e ".[dev]"
```

### 运行测试

```bash
pytest tests/
```

### 代码格式化

```bash
black src/ tests/
flake8 src/ tests/
```

## 🛠️ 技术栈

- **GUI 框架**: CustomTkinter (基于 tkinter)
- **音频处理**: Mutagen
- **图像处理**: Pillow
- **主题系统**: 自定义实现
- **跨平台**: Python 标准库

## 📝 功能规划

### 已实现 ✅
- [x] 多格式音频文件支持
- [x] 元数据读取和写入
- [x] 封面艺术处理
- [x] 多主题 GUI
- [x] Windows 平台优化
- [x] Android 平台优化
- [x] 批量编辑基础功能

### 开发中 🚧
- [ ] 完整的批量编辑界面
- [ ] 歌词编辑器
- [ ] 元数据自动获取（MusicBrainz）
- [ ] 音频波形可视化
- [ ] 播放列表支持

### 计划中 📋
- [ ] 移动端应用 (Android/iOS)
- [ ] 云同步功能
- [ ] 插件系统
- [ ] 多语言支持


## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [Mutagen](https://github.com/quodlibet/mutagen) - 强大的音频元数据处理库
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - 现代化 tkinter 界面
- [Pillow](https://python-pillow.org/) - Python 图像处理库

### Powered by X1anLu0
