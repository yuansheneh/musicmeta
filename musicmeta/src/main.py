"""
MusicMeta - 跨平台音乐元数据编辑器

主程序入口
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    """主函数"""
    # 导入平台优化器
    from src.platforms import get_platform_optimizer
    
    optimizer = get_platform_optimizer()
    optimizer.initialize()
    
    # 启动 GUI
    from src.gui.main_window import MainWindow
    
    app = MainWindow()
    app.protocol("WM_DELETE_WINDOW", lambda: on_closing(app, optimizer))
    app.mainloop()


def on_closing(app, optimizer):
    """应用关闭处理"""
    optimizer.cleanup()
    app.destroy()


def run_cli():
    """命令行模式"""
    import argparse
    
    parser = argparse.ArgumentParser(description='MusicMeta - 音乐元数据编辑器')
    parser.add_argument('file', nargs='?', help='音频文件路径')
    parser.add_argument('--gui', action='store_true', help='启动 GUI 界面')
    parser.add_argument('--info', action='store_true', help='显示文件信息')
    parser.add_argument('--output', '-o', help='输出文件路径')
    
    args = parser.parse_args()
    
    if args.gui or not args.file:
        # 启动 GUI
        main()
    else:
        # 命令行模式
        from src.core.audio_loader import AudioLoader
        
        loader = AudioLoader()
        
        if args.info:
            # 显示信息
            metadata = loader.load(args.file)
            
            print(f"\n文件：{metadata.file_path}")
            print(f"格式：{metadata.codec}")
            print(f"时长：{metadata.duration:.2f}s" if metadata.duration else "")
            print(f"比特率：{metadata.bit_rate}kbps" if metadata.bit_rate else "")
            print(f"\n元数据:")
            print(f"  标题：{metadata.title or '未知'}")
            print(f"  艺术家：{metadata.artist or '未知'}")
            print(f"  专辑：{metadata.album or '未知'}")
            print(f"  年份：{metadata.year or '未知'}")
            print(f"  流派：{metadata.genre or '未知'}")
            print(f"  曲目：{metadata.track_number or '未知'}")
            print(f"  封面：{'有' if metadata.has_cover() else '无'}")
            print()


if __name__ == "__main__":
    main()
