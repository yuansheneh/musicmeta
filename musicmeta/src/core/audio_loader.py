"""
音频文件加载器 - 读取和写入音频元数据
支持格式：MP3, FLAC, OGG, M4A, WAV, WMA
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any, List
from PIL import Image
import io

from mutagen import File as MutagenFile, FileType, MutagenError
from mutagen.id3 import ID3, APIC, USLT, COMM
from mutagen.flac import Picture
from mutagen.mp4 import MP4Cover

from .metadata import AudioMetadata, MetadataField
from .tag_mapper import TagMapper


class AudioLoader:
    """音频文件加载器"""
    
    # 支持的格式
    SUPPORTED_FORMATS = {
        '.mp3': 'MP3',
        '.flac': 'FLAC',
        '.ogg': 'OGG Vorbis',
        '.oga': 'OGG Vorbis',
        '.opus': 'OGG Opus',
        '.m4a': 'M4A/AAC',
        '.m4b': 'M4A/AAC',
        '.aac': 'M4A/AAC',
        '.wma': 'WMA/ASF',
        '.wav': 'WAV',
        '.aiff': 'AIFF',
        '.ape': 'APE',
    }
    
    def __init__(self):
        self.tag_mapper = TagMapper()
    
    @classmethod
    def is_supported(cls, file_path: str) -> bool:
        """检查文件格式是否支持"""
        ext = Path(file_path).suffix.lower()
        return ext in cls.SUPPORTED_FORMATS
    
    @classmethod
    def get_supported_formats(cls) -> Dict[str, str]:
        """获取支持的格式列表"""
        return cls.SUPPORTED_FORMATS.copy()
    
    def load(self, file_path: str) -> AudioMetadata:
        """加载音频文件的元数据"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在：{file_path}")
        
        if not self.is_supported(file_path):
            raise ValueError(f"不支持的格式：{Path(file_path).suffix}")
        
        metadata = AudioMetadata()
        metadata.file_path = file_path
        
        try:
            audio = MutagenFile(file_path, easy=False)
            
            if audio is None:
                raise ValueError(f"无法读取音频文件：{file_path}")
            
            # 获取技术信息
            self._load_audio_info(metadata, audio)
            
            # 获取文件信息
            metadata.file_size = os.path.getsize(file_path)
            
            # 根据格式加载标签
            ext = Path(file_path).suffix.lower()
            
            if ext == '.mp3':
                self._load_id3(metadata, audio)
            elif ext in ['.flac', '.ogg', '.oga', '.opus']:
                self._load_vorbis(metadata, audio)
            elif ext in ['.m4a', '.m4b', '.aac']:
                self._load_mp4(metadata, audio)
            elif ext == '.wma':
                self._load_asf(metadata, audio)
            elif ext == '.wav':
                self._load_wav(metadata, audio)
            elif ext == '.aiff':
                self._load_aiff(metadata, audio)
            elif ext == '.ape':
                self._load_ape(metadata, audio)
            
        except MutagenError as e:
            raise ValueError(f"读取元数据失败：{str(e)}")
        
        return metadata
    
    def save(self, metadata: AudioMetadata, file_path: Optional[str] = None) -> None:
        """保存元数据到音频文件"""
        file_path = file_path or metadata.file_path
        
        if not file_path:
            raise ValueError("未指定文件路径")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在：{file_path}")
        
        ext = Path(file_path).suffix.lower()
        
        try:
            audio = MutagenFile(file_path, easy=False)
            
            if audio is None:
                raise ValueError(f"无法读取音频文件：{file_path}")
            
            # 根据格式保存标签
            if ext == '.mp3':
                self._save_id3(metadata, audio)
            elif ext in ['.flac', '.ogg', '.oga', '.opus']:
                self._save_vorbis(metadata, audio)
            elif ext in ['.m4a', '.m4b', '.aac']:
                self._save_mp4(metadata, audio)
            elif ext == '.wma':
                self._save_asf(metadata, audio)
            else:
                raise ValueError(f"不支持保存格式：{ext}")
            
            audio.save()
            
        except MutagenError as e:
            raise ValueError(f"保存元数据失败：{str(e)}")
    
    def _load_audio_info(self, metadata: AudioMetadata, audio: Any) -> None:
        """加载音频技术信息"""
        try:
            if hasattr(audio, 'info'):
                info = audio.info
                metadata.duration = getattr(info, 'length', None)
                metadata.sample_rate = getattr(info, 'sample_rate', None)
                metadata.bit_rate = getattr(info, 'bitrate', None)
                metadata.channels = getattr(info, 'channels', None)
                
                # 确定编解码器
                type_name = type(audio).__name__
                metadata.codec = self.SUPPORTED_FORMATS.get(
                    Path(metadata.file_path or '').suffix.lower(),
                    type_name
                )
                metadata.tags_type = type_name
        except Exception:
            pass
    
    def _load_id3(self, metadata: AudioMetadata, audio: Any) -> None:
        """加载 ID3 标签 (MP3)"""
        if not hasattr(audio, 'tags') or audio.tags is None:
            return
        
        tags = audio.tags
        
        # 文本标签映射
        text_frames = {
            'TIT2': 'title',
            'TPE1': 'artist',
            'TALB': 'album',
            'TPE2': 'album_artist',
            'TCOM': 'composer',
            'TPE3': 'conductor',
            'TPE4': 'remixer',
            'TPUB': 'publisher',
            'TCOP': 'copyright',
            'TENC': 'encoded_by',
            'TSSE': 'tagger',
            'TCON': 'genre',
            'TBPM': 'bpm',
            'TMOO': 'mood',
        }
        
        for frame_id, attr in text_frames.items():
            if frame_id in tags:
                value = str(tags[frame_id].text[0]) if tags[frame_id].text else None
                if value:
                    setattr(metadata, attr, value)
        
        # 年份
        if 'TDRC' in tags:
            metadata.year = self.tag_mapper.date_to_year(str(tags['TDRC']))
        elif 'TYER' in tags:
            metadata.year = self.tag_mapper.date_to_year(str(tags['TYER']))
        
        # 曲目和光盘编号
        if 'TRCK' in tags:
            track, total = self.tag_mapper.parse_track_number(str(tags['TRCK']))
            metadata.track_number = track
            metadata.track_total = total
        
        if 'TPOS' in tags:
            disc, total = self.tag_mapper.parse_disc_number(str(tags['TPOS']))
            metadata.disc_number = disc
            metadata.disc_total = total
        
        # 注释
        if 'COMM' in tags:
            metadata.comment = str(tags['COMM'].text[0]) if tags['COMM'].text else None
        
        # 歌词
        if 'USLT' in tags:
            metadata.lyrics = str(tags['USLT'].text) if tags['USLT'].text else None
        
        # 封面
        if 'APIC' in tags:
            apic = tags['APIC']
            if hasattr(apic, 'data'):
                metadata.cover_art = Image.open(io.BytesIO(apic.data))
                metadata.cover_art_mime = apic.mime
    
    def _load_vorbis(self, metadata: AudioMetadata, audio: Any) -> None:
        """加载 Vorbis Comments (FLAC, OGG)"""
        if not hasattr(audio, 'tags') or audio.tags is None:
            return
        
        tags = audio.tags
        
        # 文本标签映射
        field_map = {
            'TITLE': 'title',
            'ARTIST': 'artist',
            'ALBUM': 'album',
            'ALBUMARTIST': 'album_artist',
            'COMPOSER': 'composer',
            'CONDUCTOR': 'conductor',
            'REMIXER': 'remixer',
            'PUBLISHER': 'publisher',
            'COPYRIGHT': 'copyright',
            'ENCODEDBY': 'encoded_by',
            'TAGGER': 'tagger',
            'GENRE': 'genre',
            'COMMENT': 'comment',
            'BPM': 'bpm',
            'MOOD': 'mood',
            'LYRICS': 'lyrics',
            'RATING': 'rating',
        }
        
        for tag_name, attr in field_map.items():
            if tag_name in tags:
                value = tags[tag_name][0] if tags[tag_name] else None
                if value:
                    if attr == 'rating':
                        try:
                            setattr(metadata, attr, int(float(value)))
                        except ValueError:
                            pass
                    else:
                        setattr(metadata, attr, value)
        
        # 年份
        if 'DATE' in tags:
            metadata.year = self.tag_mapper.date_to_year(tags['DATE'][0])
        
        # 曲目编号
        if 'TRACKNUMBER' in tags:
            track, total = self.tag_mapper.parse_track_number(tags['TRACKNUMBER'][0])
            metadata.track_number = track
            if 'TRACKTOTAL' in tags:
                metadata.track_total = int(tags['TRACKTOTAL'][0])
            elif total:
                metadata.track_total = total
        
        # 光盘编号
        if 'DISCNUMBER' in tags:
            disc, total = self.tag_mapper.parse_disc_number(tags['DISCNUMBER'][0])
            metadata.disc_number = disc
            if 'DISCTOTAL' in tags:
                metadata.disc_total = int(tags['DISCTOTAL'][0])
            elif total:
                metadata.disc_total = total
        
        # 合辑
        if 'COMPILATION' in tags:
            metadata.compilation = tags['COMPILATION'][0].lower() in ['1', 'true', 'yes']
        
        # 封面
        if hasattr(audio, 'pictures') and audio.pictures:
            pic = audio.pictures[0]
            metadata.cover_art = Image.open(io.BytesIO(pic.data))
            metadata.cover_art_mime = pic.mime
    
    def _load_mp4(self, metadata: AudioMetadata, audio: Any) -> None:
        """加载 MP4 标签 (M4A/AAC)"""
        if not hasattr(audio, 'tags') or audio.tags is None:
            return
        
        tags = audio.tags
        
        # 标签映射
        field_map = {
            '\xa9nam': 'title',
            '\xa9ART': 'artist',
            '\xa9alb': 'album',
            'aART': 'album_artist',
            '\xa9wrt': 'composer',
            '\xa9dir': 'conductor',
            '\xa9rem': 'remixer',
            '\xa9pub': 'publisher',
            'cprt': 'copyright',
            '\xa9enc': 'encoded_by',
            '\xa9too': 'tagger',
            '\xa9gen': 'genre',
            '\xa9cmt': 'comment',
            '\xa9lyr': 'lyrics',
        }
        
        for tag_key, attr in field_map.items():
            if tag_key in tags and tags[tag_key]:
                value = tags[tag_key][0]
                if value:
                    setattr(metadata, attr, value)
        
        # 年份
        if '\xa9day' in tags and tags['\xa9day']:
            metadata.year = self.tag_mapper.date_to_year(str(tags['\xa9day'][0]))
        
        # 曲目编号
        if 'trkn' in tags and tags['trkn']:
            track_data = tags['trkn'][0]
            if isinstance(track_data, tuple) and len(track_data) >= 2:
                metadata.track_number = track_data[0]
                metadata.track_total = track_data[1]
        
        # 光盘编号
        if 'disk' in tags and tags['disk']:
            disc_data = tags['disk'][0]
            if isinstance(disc_data, tuple) and len(disc_data) >= 2:
                metadata.disc_number = disc_data[0]
                metadata.disc_total = disc_data[1]
        
        # BPM
        if 'tmpo' in tags and tags['tmpo']:
            metadata.bpm = float(tags['tmpo'][0])
        
        # 合辑
        if 'cpil' in tags and tags['cpil']:
            metadata.compilation = bool(tags['cpil'][0])
        
        # 封面
        if 'covr' in tags and tags['covr']:
            cover_data = tags['covr'][0]
            if cover_data:
                metadata.cover_art = Image.open(io.BytesIO(bytes(cover_data)))
                metadata.cover_art_mime = 'image/jpeg'
    
    def _load_asf(self, metadata: AudioMetadata, audio: Any) -> None:
        """加载 ASF/WMA 标签"""
        if not hasattr(audio, 'tags') or audio.tags is None:
            return
        
        tags = audio.tags
        
        # 标签映射
        field_map = {
            'Title': 'title',
            'Author': 'artist',
            'WM/AlbumTitle': 'album',
            'WM/AlbumArtist': 'album_artist',
            'WM/Composer': 'composer',
            'WM/Conductor': 'conductor',
            'WM/ModifiedBy': 'remixer',
            'WM/Publisher': 'publisher',
            'Copyright': 'copyright',
            'WM/EncodedBy': 'encoded_by',
            'WM/ToolName': 'tagger',
            'Genre': 'genre',
            'Description': 'comment',
            'WM/Lyrics': 'lyrics',
            'WM/Mood': 'mood',
        }
        
        for tag_name, attr in field_map.items():
            if tag_name in tags:
                value = str(tags[tag_name][0]) if tags[tag_name] else None
                if value:
                    setattr(metadata, attr, value)
        
        # 年份
        if 'WM/Year' in tags:
            metadata.year = self.tag_mapper.date_to_year(str(tags['WM/Year'][0]))
        
        # 曲目编号
        if 'WM/TrackNumber' in tags:
            track, total = self.tag_mapper.parse_track_number(str(tags['WM/TrackNumber'][0]))
            metadata.track_number = track
        
        if 'WM/TrackTotal' in tags:
            metadata.track_total = int(str(tags['WM/TrackTotal'][0]))
        
        # 光盘编号
        if 'WM/PartOfSet' in tags:
            disc, total = self.tag_mapper.parse_disc_number(str(tags['WM/PartOfSet'][0]))
            metadata.disc_number = disc
            metadata.disc_total = total
        
        # BPM
        if 'WM/BeatsPerMinute' in tags:
            try:
                metadata.bpm = float(str(tags['WM/BeatsPerMinute'][0]))
            except ValueError:
                pass
        
        # 评级
        if 'WM/SharedUserRating' in tags:
            try:
                metadata.rating = int(str(tags['WM/SharedUserRating'][0]))
            except ValueError:
                pass
        
        # 合辑
        if 'WM/IsCompilation' in tags:
            metadata.compilation = str(tags['WM/IsCompilation'][0]).lower() in ['1', 'true', 'yes']
        
        # 封面
        if 'WM/Picture' in tags:
            pic_data = tags['WM/Picture'][0]
            if hasattr(pic_data, 'value'):
                metadata.cover_art = Image.open(io.BytesIO(pic_data.value))
                metadata.cover_art_mime = 'image/jpeg'
    
    def _load_wav(self, metadata: AudioMetadata, audio: Any) -> None:
        """加载 WAV 标签（支持 INFO chunk）"""
        if not hasattr(audio, 'tags') or audio.tags is None:
            return
        
        tags = audio.tags
        
        # WAV INFO 标签
        info_map = {
            'INAM': 'title',
            'IART': 'artist',
            'IPRD': 'album',
            'ICMT': 'comment',
            'ICOP': 'copyright',
            'ISFT': 'tagger',
            'IGNR': 'genre',
        }
        
        for tag_id, attr in info_map.items():
            if tag_id in tags:
                value = str(tags[tag_id])
                if value:
                    setattr(metadata, attr, value)
    
    def _load_aiff(self, metadata: AudioMetadata, audio: Any) -> None:
        """加载 AIFF 标签"""
        if not hasattr(audio, 'tags') or audio.tags is None:
            return
        
        tags = audio.tags
        
        # AIFF 标签映射
        field_map = {
            'name': 'title',
            'author': 'artist',
            'album': 'album',
            'comment': 'comment',
        }
        
        for tag_key, attr in field_map.items():
            if tag_key in tags and tags[tag_key]:
                value = str(tags[tag_key])
                if value:
                    setattr(metadata, attr, value)
    
    def _load_ape(self, metadata: AudioMetadata, audio: Any) -> None:
        """加载 APE 标签"""
        if not hasattr(audio, 'tags') or audio.tags is None:
            return
        
        tags = audio.tags
        
        # APE 标签映射
        field_map = {
            'Title': 'title',
            'Artist': 'artist',
            'Album': 'album',
            'Album Artist': 'album_artist',
            'Composer': 'composer',
            'Comment': 'comment',
            'Genre': 'genre',
            'Year': 'year',
            'Track': 'track_number',
            'Disc': 'disc_number',
        }
        
        for tag_key, attr in field_map.items():
            if tag_key in tags:
                value = str(tags[tag_key][0]) if tags[tag_key] else None
                if value:
                    if attr == 'year':
                        metadata.year = self.tag_mapper.date_to_year(value)
                    elif attr in ['track_number', 'disc_number']:
                        num, _ = self.tag_mapper.parse_track_number(value)
                        setattr(metadata, attr, num)
                    else:
                        setattr(metadata, attr, value)
    
    def _save_id3(self, metadata: AudioMetadata, audio: Any) -> None:
        """保存 ID3 标签 (MP3)"""
        if not hasattr(audio, 'tags') or audio.tags is None:
            audio.add_tags()
        
        tags = audio.tags
        
        # 保存文本标签
        if metadata.title:
            tags['TIT2'] = metadata.title
        if metadata.artist:
            tags['TPE1'] = metadata.artist
        if metadata.album:
            tags['TALB'] = metadata.album
        if metadata.album_artist:
            tags['TPE2'] = metadata.album_artist
        if metadata.composer:
            tags['TCOM'] = metadata.composer
        if metadata.conductor:
            tags['TPE3'] = metadata.conductor
        if metadata.remixer:
            tags['TPE4'] = metadata.remixer
        if metadata.genre:
            tags['TCON'] = metadata.genre
        if metadata.comment:
            tags['COMM'] = metadata.comment
        if metadata.year:
            tags['TDRC'] = str(metadata.year)
        if metadata.track_number:
            tags['TRCK'] = self.tag_mapper.format_track(metadata.track_number, metadata.track_total)
        if metadata.disc_number:
            tags['TPOS'] = self.tag_mapper.format_disc(metadata.disc_number, metadata.disc_total)
        if metadata.lyrics:
            tags['USLT'] = metadata.lyrics
        if metadata.bpm:
            tags['TBPM'] = str(int(metadata.bpm))
        
        # 保存封面
        if metadata.cover_art:
            img_data = metadata.get_cover_data()
            if img_data:
                tags['APIC'] = APIC(
                    encoding=3,
                    mime='image/jpeg',
                    type=3,
                    desc='Cover',
                    data=img_data
                )
    
    def _save_vorbis(self, metadata: AudioMetadata, audio: Any) -> None:
        """保存 Vorbis Comments"""
        if not hasattr(audio, 'tags'):
            audio.add_tags()
        
        tags = audio.tags
        
        # 保存文本标签
        if metadata.title:
            tags['TITLE'] = metadata.title
        if metadata.artist:
            tags['ARTIST'] = metadata.artist
        if metadata.album:
            tags['ALBUM'] = metadata.album
        if metadata.album_artist:
            tags['ALBUMARTIST'] = metadata.album_artist
        if metadata.composer:
            tags['COMPOSER'] = metadata.composer
        if metadata.conductor:
            tags['CONDUCTOR'] = metadata.conductor
        if metadata.remixer:
            tags['REMIXER'] = metadata.remixer
        if metadata.genre:
            tags['GENRE'] = metadata.genre
        if metadata.comment:
            tags['COMMENT'] = metadata.comment
        if metadata.year:
            tags['DATE'] = str(metadata.year)
        if metadata.track_number:
            tags['TRACKNUMBER'] = str(metadata.track_number)
        if metadata.track_total:
            tags['TRACKTOTAL'] = str(metadata.track_total)
        if metadata.disc_number:
            tags['DISCNUMBER'] = str(metadata.disc_number)
        if metadata.disc_total:
            tags['DISCTOTAL'] = str(metadata.disc_total)
        if metadata.lyrics:
            tags['LYRICS'] = metadata.lyrics
        if metadata.compilation:
            tags['COMPILATION'] = '1'
        if metadata.bpm:
            tags['BPM'] = str(int(metadata.bpm))
        if metadata.rating:
            tags['RATING'] = str(metadata.rating)
        
        # 保存封面
        if metadata.cover_art:
            img_data = metadata.get_cover_data()
            if img_data:
                pic = Picture()
                pic.type = 3
                pic.desc = 'Cover'
                pic.mime = 'image/jpeg'
                pic.data = img_data
                pic_data = pic.write()
                tags['METADATA_BLOCK_PICTURE'] = [pic_data]
    
    def _save_mp4(self, metadata: AudioMetadata, audio: Any) -> None:
        """保存 MP4 标签"""
        if not hasattr(audio, 'tags'):
            audio.add_tags()
        
        tags = audio.tags
        
        # 保存文本标签
        if metadata.title:
            tags['\xa9nam'] = metadata.title
        if metadata.artist:
            tags['\xa9ART'] = metadata.artist
        if metadata.album:
            tags['\xa9alb'] = metadata.album
        if metadata.album_artist:
            tags['aART'] = metadata.album_artist
        if metadata.composer:
            tags['\xa9wrt'] = metadata.composer
        if metadata.genre:
            tags['\xa9gen'] = metadata.genre
        if metadata.comment:
            tags['\xa9cmt'] = metadata.comment
        if metadata.year:
            tags['\xa9day'] = str(metadata.year)
        if metadata.track_number:
            tags['trkn'] = [(metadata.track_number, metadata.track_total or 0)]
        if metadata.disc_number:
            tags['disk'] = [(metadata.disc_number, metadata.disc_total or 0)]
        if metadata.lyrics:
            tags['\xa9lyr'] = metadata.lyrics
        if metadata.bpm:
            tags['tmpo'] = [int(metadata.bpm)]
        if metadata.compilation:
            tags['cpil'] = True
        
        # 保存封面
        if metadata.cover_art:
            img_data = metadata.get_cover_data()
            if img_data:
                tags['covr'] = [MP4Cover(img_data, imageformat=MP4Cover.FORMAT_JPEG)]
    
    def _save_asf(self, metadata: AudioMetadata, audio: Any) -> None:
        """保存 ASF/WMA 标签"""
        if not hasattr(audio, 'tags'):
            audio.add_tags()
        
        tags = audio.tags
        
        # 保存文本标签
        if metadata.title:
            tags['Title'] = metadata.title
        if metadata.artist:
            tags['Author'] = metadata.artist
        if metadata.album:
            tags['WM/AlbumTitle'] = metadata.album
        if metadata.album_artist:
            tags['WM/AlbumArtist'] = metadata.album_artist
        if metadata.composer:
            tags['WM/Composer'] = metadata.composer
        if metadata.conductor:
            tags['WM/Conductor'] = metadata.conductor
        if metadata.remixer:
            tags['WM/ModifiedBy'] = metadata.remixer
        if metadata.genre:
            tags['Genre'] = metadata.genre
        if metadata.comment:
            tags['Description'] = metadata.comment
        if metadata.year:
            tags['WM/Year'] = str(metadata.year)
        if metadata.track_number:
            tags['WM/TrackNumber'] = str(metadata.track_number)
        if metadata.disc_number:
            tags['WM/PartOfSet'] = self.tag_mapper.format_disc(metadata.disc_number, metadata.disc_total)
        if metadata.lyrics:
            tags['WM/Lyrics'] = metadata.lyrics
        if metadata.bpm:
            tags['WM/BeatsPerMinute'] = str(int(metadata.bpm))
        if metadata.rating:
            tags['WM/SharedUserRating'] = str(metadata.rating)
        if metadata.compilation:
            tags['WM/IsCompilation'] = '1'
    
    def delete_tags(self, file_path: str, fields: Optional[List[MetadataField]] = None) -> None:
        """删除指定字段或所有标签"""
        metadata = self.load(file_path)
        
        if fields is None:
            # 删除所有标签
            ext = Path(file_path).suffix.lower()
            audio = MutagenFile(file_path, easy=False)
            
            if ext == '.mp3' and hasattr(audio, 'tags'):
                audio.delete()
            elif hasattr(audio, 'tags') and audio.tags is not None:
                audio.tags.clear()
                audio.save()
        else:
            # 删除指定字段
            for field in fields:
                metadata.set_field(field, None)
            self.save(metadata)
