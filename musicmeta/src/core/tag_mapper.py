"""
音频标签映射器 - 处理不同格式标签系统的映射
"""

from typing import Dict, List, Any, Optional
from .metadata import AudioMetadata, MetadataField


class TagMapper:
    """不同音频格式的标签映射器"""
    
    # ID3v2 (MP3) 映射
    ID3V2_MAPPING = {
        MetadataField.TITLE: 'TIT2',
        MetadataField.ARTIST: 'TPE1',
        MetadataField.ALBUM: 'TALB',
        MetadataField.ALBUM_ARTIST: 'TPE2',
        MetadataField.YEAR: 'TDRC',
        MetadataField.TRACK_NUMBER: 'TRCK',
        MetadataField.TRACK_TOTAL: 'TRCK',
        MetadataField.DISC_NUMBER: 'TPOS',
        MetadataField.DISC_TOTAL: 'TPOS',
        MetadataField.GENRE: 'TCON',
        MetadataField.COMMENT: 'COMM',
        MetadataField.COMPOSER: 'TCOM',
        MetadataField.CONDUCTOR: 'TPE3',
        MetadataField.REMIXER: 'TPE4',
        MetadataField.PUBLISHER: 'TPUB',
        MetadataField.COPYRIGHT: 'TCOP',
        MetadataField.ENCODED_BY: 'TENC',
        MetadataField.TAGGER: 'TSSE',
        MetadataField.BPM: 'TBPM',
        MetadataField.MOOD: 'TMOO',
        MetadataField.LYRICS: 'USLT',
        MetadataField.COVER_ART: 'APIC',
    }
    
    # Vorbis Comments (FLAC, OGG) 映射
    VORBIS_MAPPING = {
        MetadataField.TITLE: 'TITLE',
        MetadataField.ARTIST: 'ARTIST',
        MetadataField.ALBUM: 'ALBUM',
        MetadataField.ALBUM_ARTIST: 'ALBUMARTIST',
        MetadataField.YEAR: 'DATE',
        MetadataField.TRACK_NUMBER: 'TRACKNUMBER',
        MetadataField.TRACK_TOTAL: 'TRACKTOTAL',
        MetadataField.DISC_NUMBER: 'DISCNUMBER',
        MetadataField.DISC_TOTAL: 'DISCTOTAL',
        MetadataField.GENRE: 'GENRE',
        MetadataField.COMMENT: 'COMMENT',
        MetadataField.COMPILATION: 'COMPILATION',
        MetadataField.COMPOSER: 'COMPOSER',
        MetadataField.CONDUCTOR: 'CONDUCTOR',
        MetadataField.REMIXER: 'REMIXER',
        MetadataField.PUBLISHER: 'PUBLISHER',
        MetadataField.COPYRIGHT: 'COPYRIGHT',
        MetadataField.ENCODED_BY: 'ENCODEDBY',
        MetadataField.TAGGER: 'TAGGER',
        MetadataField.BPM: 'BPM',
        MetadataField.MOOD: 'MOOD',
        MetadataField.RATING: 'RATING',
        MetadataField.LYRICS: 'LYRICS',
        MetadataField.COVER_ART: 'METADATA_BLOCK_PICTURE',
    }
    
    # MP4 (M4A/AAC) 映射
    MP4_MAPPING = {
        MetadataField.TITLE: '\xa9nam',
        MetadataField.ARTIST: '\xa9ART',
        MetadataField.ALBUM: '\xa9alb',
        MetadataField.ALBUM_ARTIST: 'aART',
        MetadataField.YEAR: '\xa9day',
        MetadataField.TRACK_NUMBER: 'trkn',
        MetadataField.TRACK_TOTAL: 'trkn',
        MetadataField.DISC_NUMBER: 'disk',
        MetadataField.DISC_TOTAL: 'disk',
        MetadataField.GENRE: '\xa9gen',
        MetadataField.COMMENT: '\xa9cmt',
        MetadataField.COMPILATION: 'cpil',
        MetadataField.COMPOSER: '\xa9wrt',
        MetadataField.CONDUCTOR: '\xa9dir',
        MetadataField.REMIXER: '\xa9rem',
        MetadataField.PUBLISHER: '\xa9pub',
        MetadataField.COPYRIGHT: 'cprt',
        MetadataField.ENCODED_BY: '\xa9enc',
        MetadataField.TAGGER: '\xa9too',
        MetadataField.BPM: 'tmpo',
        MetadataField.LYRICS: '\xa9lyr',
        MetadataField.COVER_ART: 'covr',
    }
    
    # ASF (WMA) 映射
    ASF_MAPPING = {
        MetadataField.TITLE: 'Title',
        MetadataField.ARTIST: 'Author',
        MetadataField.ALBUM: 'WM/AlbumTitle',
        MetadataField.ALBUM_ARTIST: 'WM/AlbumArtist',
        MetadataField.YEAR: 'WM/Year',
        MetadataField.TRACK_NUMBER: 'WM/TrackNumber',
        MetadataField.TRACK_TOTAL: 'WM/TrackTotal',
        MetadataField.DISC_NUMBER: 'WM/PartOfSet',
        MetadataField.DISC_TOTAL: 'WM/PartOfSet',
        MetadataField.GENRE: 'Genre',
        MetadataField.COMMENT: 'Description',
        MetadataField.COMPILATION: 'WM/IsCompilation',
        MetadataField.COMPOSER: 'WM/Composer',
        MetadataField.CONDUCTOR: 'WM/Conductor',
        MetadataField.REMIXER: 'WM/ModifiedBy',
        MetadataField.PUBLISHER: 'WM/Publisher',
        MetadataField.COPYRIGHT: 'Copyright',
        MetadataField.ENCODED_BY: 'WM/EncodedBy',
        MetadataField.TAGGER: 'WM/ToolName',
        MetadataField.BPM: 'WM/BeatsPerMinute',
        MetadataField.MOOD: 'WM/Mood',
        MetadataField.RATING: 'WM/SharedUserRating',
        MetadataField.LYRICS: 'WM/Lyrics',
        MetadataField.COVER_ART: 'WM/Picture',
    }
    
    @classmethod
    def get_mapping(cls, format_type: str) -> Dict[MetadataField, str]:
        """获取指定格式的标签映射"""
        mappings = {
            'id3': cls.ID3V2_MAPPING,
            'mp3': cls.ID3V2_MAPPING,
            'vorbis': cls.VORBIS_MAPPING,
            'flac': cls.VORBIS_MAPPING,
            'ogg': cls.VORBIS_MAPPING,
            'opus': cls.VORBIS_MAPPING,
            'mp4': cls.MP4_MAPPING,
            'm4a': cls.MP4_MAPPING,
            'aac': cls.MP4_MAPPING,
            'asf': cls.ASF_MAPPING,
            'wma': cls.ASF_MAPPING,
            'wav': {},  # WAV 通常不支持标签
        }
        return mappings.get(format_type.lower(), {})
    
    @classmethod
    def parse_track_number(cls, value: str) -> tuple:
        """解析曲目编号（支持 "1/10" 格式）"""
        if not value:
            return None, None
        
        if '/' in str(value):
            parts = str(value).split('/')
            try:
                track = int(parts[0])
                total = int(parts[1]) if len(parts) > 1 else None
                return track, total
            except (ValueError, IndexError):
                return None, None
        else:
            try:
                return int(value), None
            except ValueError:
                return None, None
    
    @classmethod
    def parse_disc_number(cls, value: str) -> tuple:
        """解析光盘编号（支持 "1/2" 格式）"""
        return cls.parse_track_number(value)
    
    @classmethod
    def format_track(cls, track: Optional[int], total: Optional[int] = None) -> Optional[str]:
        """格式化曲目编号"""
        if track is None:
            return None
        if total is not None:
            return f"{track}/{total}"
        return str(track)
    
    @classmethod
    def format_disc(cls, disc: Optional[int], total: Optional[int] = None) -> Optional[str]:
        """格式化光盘编号"""
        return cls.format_track(disc, total)
    
    @classmethod
    def year_to_date(cls, year: Optional[int]) -> Optional[str]:
        """将年份转换为日期字符串"""
        if year is None:
            return None
        return str(year)
    
    @classmethod
    def date_to_year(cls, date_str: Optional[str]) -> Optional[int]:
        """从日期字符串提取年份"""
        if not date_str:
            return None
        try:
            # 处理 "YYYY", "YYYY-MM", "YYYY-MM-DD" 等格式
            return int(str(date_str)[:4])
        except (ValueError, IndexError):
            return None
