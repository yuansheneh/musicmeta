"""
测试核心元数据处理功能
"""

import unittest
import os
import sys
import tempfile
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入被测试模块
from src.core.metadata import AudioMetadata, MetadataField
from src.core.tag_mapper import TagMapper
from src.core.audio_loader import AudioLoader


class TestAudioMetadata(unittest.TestCase):
    """测试 AudioMetadata 类"""
    
    def setUp(self):
        """测试前准备"""
        self.metadata = AudioMetadata()
    
    def test_default_values(self):
        """测试默认值"""
        self.assertIsNone(self.metadata.title)
        self.assertIsNone(self.metadata.artist)
        self.assertFalse(self.metadata.compilation)
    
    def test_set_field(self):
        """测试设置字段"""
        self.metadata.set_field(MetadataField.TITLE, "Test Song")
        self.assertEqual(self.metadata.title, "Test Song")
    
    def test_get_field(self):
        """测试获取字段"""
        self.metadata.title = "Test Song"
        self.assertEqual(self.metadata.get_field(MetadataField.TITLE), "Test Song")
    
    def test_has_cover(self):
        """测试封面检测"""
        self.assertFalse(self.metadata.has_cover())
    
    def test_to_dict(self):
        """测试转换为字典"""
        self.metadata.title = "Test"
        self.metadata.artist = "Artist"
        
        result = self.metadata.to_dict()
        self.assertEqual(result['title'], "Test")
        self.assertEqual(result['artist'], "Artist")


class TestTagMapper(unittest.TestCase):
    """测试 TagMapper 类"""
    
    def test_parse_track_number_simple(self):
        """测试简单曲目编号解析"""
        track, total = TagMapper.parse_track_number("5")
        self.assertEqual(track, 5)
        self.assertIsNone(total)
    
    def test_parse_track_number_with_total(self):
        """测试带总数的曲目编号解析"""
        track, total = TagMapper.parse_track_number("5/12")
        self.assertEqual(track, 5)
        self.assertEqual(total, 12)
    
    def test_format_track(self):
        """测试曲目编号格式化"""
        result = TagMapper.format_track(5, 12)
        self.assertEqual(result, "5/12")
    
    def test_year_conversion(self):
        """测试年份转换"""
        self.assertEqual(TagMapper.year_to_date(2023), "2023")
        self.assertEqual(TagMapper.date_to_year("2023"), 2023)
        self.assertEqual(TagMapper.date_to_year("2023-05-15"), 2023)


class TestAudioLoader(unittest.TestCase):
    """测试 AudioLoader 类"""
    
    def setUp(self):
        """测试前准备"""
        self.loader = AudioLoader()
        self.test_file = None
    
    def tearDown(self):
        """测试后清理"""
        if self.test_file and os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_is_supported(self):
        """测试格式支持检测"""
        self.assertTrue(AudioLoader.is_supported("test.mp3"))
        self.assertTrue(AudioLoader.is_supported("test.flac"))
        self.assertTrue(AudioLoader.is_supported("test.ogg"))
        self.assertFalse(AudioLoader.is_supported("test.txt"))
    
    def test_get_supported_formats(self):
        """测试获取支持的格式"""
        formats = AudioLoader.get_supported_formats()
        self.assertIn('.mp3', formats)
        self.assertIn('.flac', formats)
        self.assertIn('.ogg', formats)
    
    def test_load_nonexistent_file(self):
        """测试加载不存在的文件"""
        with self.assertRaises(FileNotFoundError):
            self.loader.load("nonexistent_file.mp3")


class TestBatchEditor(unittest.TestCase):
    """测试批量编辑器"""
    
    def setUp(self):
        """测试前准备"""
        from src.utils.batch_editor import BatchEditor, BatchOperation
        self.editor = BatchEditor()
        self.BatchOperation = BatchOperation
    
    def test_create_operation(self):
        """测试创建操作"""
        op = self.BatchOperation(
            field=MetadataField.TITLE,
            value="Test",
            operation='set'
        )
        self.assertEqual(op.field, MetadataField.TITLE)
        self.assertEqual(op.value, "Test")


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试
    suite.addTests(loader.loadTestsFromTestCase(TestAudioMetadata))
    suite.addTests(loader.loadTestsFromTestCase(TestTagMapper))
    suite.addTests(loader.loadTestsFromTestCase(TestAudioLoader))
    suite.addTests(loader.loadTestsFromTestCase(TestBatchEditor))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
