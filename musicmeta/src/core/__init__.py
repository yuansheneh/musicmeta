"""
MusicMeta Core - 核心元数据处理引擎
支持多种音频格式：MP3, FLAC, OGG, M4A, WAV, WMA
"""

from .metadata import AudioMetadata, MetadataField
from .audio_loader import AudioLoader
from .tag_mapper import TagMapper

__all__ = ['AudioMetadata', 'MetadataField', 'AudioLoader', 'TagMapper']
