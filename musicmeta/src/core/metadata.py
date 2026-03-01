"""
音频元数据模型定义
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from enum import Enum
from PIL import Image
import io


class MetadataField(Enum):
    """元数据字段类型"""
    TITLE = "title"
    ARTIST = "artist"
    ALBUM = "album"
    ALBUM_ARTIST = "album_artist"
    YEAR = "year"
    TRACK_NUMBER = "track_number"
    TRACK_TOTAL = "track_total"
    DISC_NUMBER = "disc_number"
    DISC_TOTAL = "disc_total"
    GENRE = "genre"
    COMMENT = "comment"
    COMPILATION = "compilation"
    COVER_ART = "cover_art"
    LYRICS = "lyrics"
    COMPOSER = "composer"
    CONDUCTOR = "conductor"
    REMIXER = "remixer"
    PUBLISHER = "publisher"
    COPYRIGHT = "copyright"
    ENCODED_BY = "encoded_by"
    TAGGER = "tagger"
    BPM = "bpm"
    MOOD = "mood"
    RATING = "rating"


@dataclass
class AudioMetadata:
    """音频元数据容器"""
    
    # 基本信息
    title: Optional[str] = None
    artist: Optional[str] = None
    album: Optional[str] = None
    album_artist: Optional[str] = None
    
    # 编号信息
    year: Optional[int] = None
    track_number: Optional[int] = None
    track_total: Optional[int] = None
    disc_number: Optional[int] = None
    disc_total: Optional[int] = None
    
    # 分类信息
    genre: Optional[str] = None
    comment: Optional[str] = None
    compilation: bool = False
    
    # 高级信息
    composer: Optional[str] = None
    conductor: Optional[str] = None
    remixer: Optional[str] = None
    publisher: Optional[str] = None
    copyright: Optional[str] = None
    encoded_by: Optional[str] = None
    tagger: Optional[str] = None
    
    # 媒体信息
    bpm: Optional[float] = None
    mood: Optional[str] = None
    rating: Optional[int] = None
    lyrics: Optional[str] = None
    
    # 封面艺术
    cover_art: Optional[Image.Image] = None
    cover_art_mime: Optional[str] = None
    
    # 技术信息
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    duration: Optional[float] = None
    sample_rate: Optional[int] = None
    bit_rate: Optional[int] = None
    channels: Optional[int] = None
    codec: Optional[str] = None
    tags_type: Optional[str] = None
    
    # 扩展字段
    extra_fields: Dict[str, Any] = field(default_factory=dict)
    
    def get_field(self, field: MetadataField) -> Any:
        """获取指定字段的值"""
        return getattr(self, field.value, None)
    
    def set_field(self, field: MetadataField, value: Any) -> None:
        """设置指定字段的值"""
        if hasattr(self, field.value):
            setattr(self, field.value, value)
        else:
            self.extra_fields[field.value] = value
    
    def has_cover(self) -> bool:
        """检查是否有封面"""
        return self.cover_art is not None
    
    def get_cover_data(self) -> Optional[bytes]:
        """获取封面二进制数据"""
        if not self.cover_art:
            return None
        
        buffer = io.BytesIO()
        format = 'PNG' if self.cover_art_mime == 'image/png' else 'JPEG'
        self.cover_art.save(buffer, format=format)
        return buffer.getvalue()
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'title': self.title,
            'artist': self.artist,
            'album': self.album,
            'album_artist': self.album_artist,
            'year': self.year,
            'track_number': self.track_number,
            'track_total': self.track_total,
            'disc_number': self.disc_number,
            'disc_total': self.disc_total,
            'genre': self.genre,
            'comment': self.comment,
            'compilation': self.compilation,
            'composer': self.composer,
            'conductor': self.conductor,
            'remixer': self.remixer,
            'publisher': self.publisher,
            'copyright': self.copyright,
            'encoded_by': self.encoded_by,
            'tagger': self.tagger,
            'bpm': self.bpm,
            'mood': self.mood,
            'rating': self.rating,
            'lyrics': self.lyrics,
            'has_cover': self.has_cover(),
            'file_path': self.file_path,
            'file_size': self.file_size,
            'duration': self.duration,
            'sample_rate': self.sample_rate,
            'bit_rate': self.bit_rate,
            'channels': self.channels,
            'codec': self.codec,
            'tags_type': self.tags_type,
        }
    
    def copy_from(self, other: 'AudioMetadata', fields: Optional[List[MetadataField]] = None) -> None:
        """从另一个元数据对象复制字段"""
        if fields is None:
            fields = list(MetadataField)
        
        for fld in fields:
            value = other.get_field(fld)
            if value is not None:
                self.set_field(fld, value)
    
    def __str__(self) -> str:
        artist_title = f"{self.artist} - {self.title}" if self.artist and self.title else self.title or "Unknown"
        return f"<AudioMetadata: {artist_title}>"
