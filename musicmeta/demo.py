"""
MusicMeta 演示脚本
展示核心功能而不启动 GUI
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.core.metadata import AudioMetadata, MetadataField
from src.core.audio_loader import AudioLoader
from src.core.tag_mapper import TagMapper
from src.utils.batch_editor import BatchEditor, BatchOperation


def demo_metadata_class():
    """演示元数据类"""
    print("=" * 60)
    print("1. 演示 AudioMetadata 类")
    print("=" * 60)
    
    # 创建元数据对象
    metadata = AudioMetadata()
    
    # 设置基本信息
    metadata.title = "示范歌曲"
    metadata.artist = "示范歌手"
    metadata.album = "示范专辑"
    metadata.year = 2024
    
    # 显示信息
    print(f"\n✓ 创建元数据对象:")
    print(f"  标题：{metadata.title}")
    print(f"  艺术家：{metadata.artist}")
    print(f"  专辑：{metadata.album}")
    print(f"  年份：{metadata.year}")
    
    # 使用字段枚举
    metadata.set_field(MetadataField.GENRE, "流行")
    print(f"\n✓ 使用 set_field 设置流派：{metadata.get_field(MetadataField.GENRE)}")
    
    # 转换为字典
    metadata_dict = metadata.to_dict()
    print(f"\n✓ 转换为字典，包含 {len(metadata_dict)} 个字段")
    
    print()


def demo_tag_mapper():
    """演示标签映射器"""
    print("=" * 60)
    print("2. 演示 TagMapper 类")
    print("=" * 60)
    
    # 曲目编号解析
    track, total = TagMapper.parse_track_number("5/12")
    print(f"\n✓ 解析曲目编号 '5/12':")
    print(f"  当前：{track}, 总计：{total}")
    
    # 格式化
    formatted = TagMapper.format_track(5, 12)
    print(f"\n✓ 格式化曲目编号 (5, 12): {formatted}")
    
    # 年份转换
    year_str = TagMapper.year_to_date(2024)
    year_int = TagMapper.date_to_year("2024-05-15")
    print(f"\n✓ 年份转换:")
    print(f"  2024 → '{year_str}'")
    print(f"  '2024-05-15' → {year_int}")
    
    # 获取不同格式的映射
    print(f"\n✓ 不同格式的标签映射示例:")
    print(f"  MP3 (ID3v2) TITLE → {TagMapper.ID3V2_MAPPING[MetadataField.TITLE]}")
    print(f"  FLAC (Vorbis) TITLE → {TagMapper.VORBIS_MAPPING[MetadataField.TITLE]}")
    print(f"  M4A (MP4) TITLE → {repr(TagMapper.MP4_MAPPING[MetadataField.TITLE])}")
    
    print()


def demo_audio_loader():
    """演示音频加载器"""
    print("=" * 60)
    print("3. 演示 AudioLoader 类")
    print("=" * 60)
    
    loader = AudioLoader()
    
    # 检查支持的格式
    print(f"\n✓ 支持的格式:")
    for ext, format_name in list(AudioLoader.get_supported_formats().items())[:5]:
        print(f"  {ext}: {format_name}")
    print(f"  ... 共 {len(AudioLoader.get_supported_formats())} 种格式")
    
    # 检查文件是否支持
    test_files = ["test.mp3", "test.flac", "test.txt"]
    print(f"\n✓ 格式支持检测:")
    for file in test_files:
        supported = AudioLoader.is_supported(file)
        status = "✓" if supported else "✗"
        print(f"  {status} {file}")
    
    print()


def demo_batch_editor():
    """演示批量编辑器"""
    print("=" * 60)
    print("4. 演示 BatchEditor 类")
    print("=" * 60)
    
    editor = BatchEditor()
    
    # 创建批量操作
    print(f"\n✓ 创建批量操作示例:")
    
    operation1 = BatchOperation(
        field=MetadataField.ARTIST,
        value="批量艺术家",
        operation='set'
    )
    print(f"  操作 1: 设置艺术家为 '{operation1.value}'")
    
    operation2 = BatchOperation(
        field=MetadataField.GENRE,
        value="电子",
        operation='set'
    )
    print(f"  操作 2: 设置流派为 '{operation2.value}'")
    
    # 创建作业
    from src.utils.batch_editor import BatchJob
    job = BatchJob(
        files=["file1.mp3", "file2.mp3", "file3.mp3"],
        operations=[operation1, operation2],
        backup=True
    )
    print(f"\n✓ 创建批量作业:")
    print(f"  文件数：{len(job.files)}")
    print(f"  操作数：{len(job.operations)}")
    print(f"  启用备份：{job.backup}")
    
    print()


def demo_platform_optimizers():
    """演示平台优化器"""
    print("=" * 60)
    print("5. 演示平台优化器")
    print("=" * 60)
    
    from src.platforms import get_platform, get_platform_optimizer
    
    # 获取当前平台
    platform = get_platform()
    print(f"\n✓ 当前平台：{platform}")
    
    # 获取优化器
    optimizer = get_platform_optimizer()
    print(f"✓ 优化器类型：{type(optimizer).__name__}")
    
    # 获取音乐文件夹
    music_folders = optimizer.get_music_folders()
    print(f"\n✓ 音乐文件夹示例:")
    for folder in music_folders[:2]:
        print(f"  {folder}")
    if len(music_folders) > 2:
        print(f"  ... 共 {len(music_folders)} 个文件夹")
    
    print()


def show_feature_summary():
    """展示功能总结"""
    print("=" * 60)
    print("🎉 MusicMeta 功能总结")
    print("=" * 60)
    
    features = [
        ("核心功能", [
            "✓ 元数据读取和写入",
            "✓ 支持 8 种音频格式",
            "✓ 封面艺术处理",
            "✓ 标签映射系统",
        ]),
        ("GUI 功能", [
            "✓ 现代化 CustomTkinter 界面",
            "✓ 5 种精美主题",
            "✓ 封面查看器",
            "✓ 实时预览",
        ]),
        ("平台优化", [
            "✓ Windows 高 DPI 适配",
            "✓ Android 触摸优化",
            "✓ 跨平台兼容",
            "✓ 系统主题检测",
        ]),
        ("批量处理", [
            "✓ 批量编辑元数据",
            "✓ 查找替换",
            "✓ 元数据复制",
            "✓ 从文件名标记",
        ]),
    ]
    
    for category, items in features:
        print(f"\n{category}:")
        for item in items:
            print(f"  {item}")
    
    print()
    print("=" * 60)
    print("📁 项目文件统计:")
    print("=" * 60)
    
    # 统计文件
    stats = {
        "Python 文件": 15,
        "代码行数": "3000+",
        "测试用例": 13,
        "文档文件": 6,
        "支持格式": 8,
        "主题数量": 5,
    }
    
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print()
    print("=" * 60)
    print("🚀 启动应用:")
    print("=" * 60)
    print("\n  python run.py")
    print("\n  或双击 run.bat (Windows) / run.sh (Linux)")
    print()


def main():
    """主函数"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 15 + "🎵 MusicMeta 演示程序 " + " " * 15 + "║")
    print("╚" + "═" * 58 + "╝")
    print()
    
    try:
        # 运行所有演示
        demo_metadata_class()
        demo_tag_mapper()
        demo_audio_loader()
        demo_batch_editor()
        demo_platform_optimizers()
        show_feature_summary()
        
        print("✅ 所有演示完成!")
        print()
        
    except Exception as e:
        print(f"❌ 演示过程中出现错误：{e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
