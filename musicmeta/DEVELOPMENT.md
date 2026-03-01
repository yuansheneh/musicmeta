# 📋 MusicMeta 项目开发文档

## 项目概述

MusicMeta 是一个功能完整的跨平台音乐元数据编辑器，采用 Python 开发，使用 CustomTkinter 构建现代化 GUI 界面。

### 核心目标

1. ✅ **跨平台支持**: Windows、Android、macOS、Linux
2. ✅ **多格式支持**: MP3、FLAC、OGG、M4A、WMA 等
3. ✅ **华丽界面**: 多主题、现代化设计
4. ✅ **平台优化**: 针对 Windows 和 Android 特殊优化
5. ✅ **批量处理**: 高效的批量编辑功能

## 技术架构

```
┌─────────────────────────────────────────┐
│           GUI Layer (CustomTkinter)      │
│  ┌──────────┬──────────┬────────────┐  │
│  │ 主窗口   │ 组件库   │ 主题管理   │  │
│  └──────────┴──────────┴────────────┘  │
├─────────────────────────────────────────┤
│         Platform Abstraction Layer       │
│  ┌──────────┬──────────┬────────────┐  │
│  │ Windows  │ Android  │ Base       │  │
│  │ 优化器   │ 优化器   │ 优化器     │  │
│  └──────────┴──────────┴────────────┘  │
├─────────────────────────────────────────┤
│          Core Engine (Mutagen)           │
│  ┌──────────┬──────────┬────────────┐  │
│  │ 元数据   │ 音频加载 │ 标签映射   │  │
│  │ 模型     │ 器       │ 器         │  │
│  └──────────┴──────────┴────────────┘  │
├─────────────────────────────────────────┤
│           Utilities                      │
│  ┌──────────┬──────────┬────────────┐  │
│  │ 批量编辑 │ 文件工具 │ 图像处理   │  │
│  └──────────┴──────────┴────────────┘  │
└─────────────────────────────────────────┘
```

## 已实现功能

### 核心功能 ✅

- [x] 元数据读取和写入
- [x] 支持 8 种音频格式
- [x] 封面艺术处理
- [x] 标签映射系统
- [x] 批量编辑引擎

### GUI 功能 ✅

- [x] 主窗口界面
- [x] 元数据编辑器组件
- [x] 封面查看器
- [x] 文件列表面板
- [x] 状态栏
- [x] 5 种精美主题
- [x] 实时预览

### 平台优化 ✅

**Windows**:
- [x] 高 DPI 适配
- [x] 暗色标题栏
- [x] 系统主题检测
- [x] 文件管理器集成
- [x] 右键菜单（框架）

**Android**:
- [x] 触摸优化
- [x] 存储访问框架
- [x] 后台扫描
- [x] 媒体扫描器集成

### 工具功能 ✅

- [x] 批量编辑器
- [x] 查找替换
- [x] 元数据复制
- [x] 从文件名标记
- [x] 文件备份

## 文件结构

```
musicmeta/
├── src/                      # 源代码
│   ├── __init__.py
│   ├── main.py               # 程序入口
│   ├── core/                 # 核心引擎
│   │   ├── __init__.py
│   │   ├── metadata.py       # 元数据模型
│   │   ├── audio_loader.py   # 音频加载器
│   │   └── tag_mapper.py     # 标签映射器
│   ├── gui/                  # GUI 层
│   │   ├── __init__.py
│   │   ├── main_window.py    # 主窗口
│   │   ├── components.py     # UI 组件
│   │   └── theme_manager.py  # 主题管理
│   ├── platforms/            # 平台优化
│   │   ├── __init__.py
│   │   ├── base_optimizer.py
│   │   ├── windows_optimizer.py
│   │   └── android_optimizer.py
│   └── utils/                # 工具
│       ├── __init__.py
│       └── batch_editor.py   # 批量编辑器
├── tests/                    # 测试
│   ├── __init__.py
│   └── test_core.py
├── assets/                   # 资源文件
│   ├── icons/
│   └── themes/
├── requirements.txt          # Python 依赖
├── pyproject.toml           # 项目配置
├── README.md                # 项目说明
├── QUICKSTART.md            # 快速开始
├── INTERFACE.md             # 界面说明
├── run.py                   # 启动脚本
├── run.bat                  # Windows 启动
└── run.sh                   # Linux 启动
```

## 核心类说明

### AudioMetadata
**位置**: `src/core/metadata.py`

数据类，存储所有元数据字段。

**主要属性**:
- `title`, `artist`, `album`: 基本信息
- `year`, `track_number`, `disc_number`: 编号
- `cover_art`: PIL Image 对象
- `duration`, `bit_rate`: 技术信息

**方法**:
- `get_field(field)`: 获取字段值
- `set_field(field, value)`: 设置字段值
- `to_dict()`: 转换为字典
- `copy_from(other)`: 从其他对象复制

### AudioLoader
**位置**: `src/core/audio_loader.py`

音频文件加载器，处理所有格式的读写。

**主要方法**:
- `load(file_path)`: 加载元数据
- `save(metadata)`: 保存元数据
- `is_supported(ext)`: 检查格式支持

**支持的格式**:
- MP3 → ID3v2
- FLAC/OGG → Vorbis Comments
- M4A → MP4 标签
- WMA → ASF 标签

### TagMapper
**位置**: `src/core/tag_mapper.py`

不同格式标签系统的映射器。

**映射表**:
- `ID3V2_MAPPING`: MP3 标签
- `VORBIS_MAPPING`: FLAC/OGG 标签
- `MP4_MAPPING`: M4A 标签
- `ASF_MAPPING`: WMA 标签

### MainWindow
**位置**: `src/gui/main_window.py`

应用主窗口。

**布局**:
- 左侧边栏：操作按钮、主题选择
- 顶部：文件信息栏
- 中央：封面查看器 + 元数据编辑器
- 底部：状态栏

### ThemeManager
**位置**: `src/gui/theme_manager.py`

主题管理系统。

**内置主题**:
- dark, light, ocean, sunset, forest

**方法**:
- `apply_theme(name)`: 应用主题
- `get_color(name)`: 获取颜色值

### Platform Optimizers
**位置**: `src/platforms/`

平台特定的优化器。

**基类**: `BaseOptimizer`
- `initialize()`: 初始化
- `get_music_folders()`: 获取音乐文件夹
- `optimize_for_high_dpi()`: 高 DPI 优化

**Windows**: `WindowsOptimizer`
- 注册表集成
- 文件管理器集成
- DPI 感知

**Android**: `AndroidOptimizer`
- 存储访问
- 媒体扫描器
- 触摸优化

## 数据流

### 加载文件流程

```
用户打开文件
    ↓
AudioLoader.load(file_path)
    ↓
检测文件格式
    ↓
调用对应加载器 (_load_id3, _load_vorbis, etc.)
    ↓
解析标签 → AudioMetadata
    ↓
更新 GUI (封面、编辑器)
    ↓
显示完成
```

### 保存文件流程

```
用户点击保存
    ↓
从编辑器收集数据 → AudioMetadata
    ↓
AudioLoader.save(metadata)
    ↓
调用对应保存器 (_save_id3, etc.)
    ↓
写入文件
    ↓
显示完成
```

## 测试

### 运行测试

```bash
# 运行所有测试
python tests/test_core.py

# 运行特定测试类
python -m unittest tests.test_core.TestAudioMetadata
```

### 测试覆盖

- ✅ AudioMetadata: 字段操作、序列化
- ✅ TagMapper: 编号解析、格式化
- ✅ AudioLoader: 格式检测、文件加载
- ✅ BatchEditor: 批量操作

## 依赖说明

### 核心依赖

- **customtkinter** (5.2.1): GUI 框架
- **mutagen** (1.47.0): 音频元数据处理
- **Pillow** (10.1.0): 图像处理
- **darkdetect** (0.8.0): 系统主题检测

### 可选依赖

- **pywin32**: Windows 特定功能
- **android-storage**: Android 存储访问

## 性能考虑

### 优化措施

1. **懒加载**: 封面图片按需加载
2. **并行处理**: 批量操作使用线程池
3. **缓存**: 最近文件列表缓存
4. **增量更新**: GUI 组件增量刷新

### 限制

- 单次批量处理建议 < 1000 文件
- 封面图片建议 < 2MB
- 大文件夹扫描可能需要数分钟

## 未来规划

### 短期 (v1.1)

- [ ] 完整的批量编辑 GUI
- [ ] 歌词编辑器
- [ ] 拖放上传封面
- [ ] 右键菜单集成

### 中期 (v1.2)

- [ ] MusicBrainz 自动标记
- [ ] 音频波形可视化
- [ ] 播放列表支持
- [ ] 多语言支持

### 长期 (v2.0)

- [ ] 移动端应用
- [ ] 云同步
- [ ] 插件系统
- [ ] Web 版本

## 贡献指南

### 代码风格

- 遵循 PEP 8
- 使用 type hints
- 编写文档字符串
- 添加单元测试

### 提交规范

```
feat: 添加新功能
fix: 修复 bug
docs: 文档更新
style: 代码格式化
refactor: 重构
test: 添加测试
chore: 构建/工具
```

## 许可证

MIT License - 详见 LICENSE 文件

**开发团队**: MusicMeta Team  
**最后更新**: 2026-03-01
