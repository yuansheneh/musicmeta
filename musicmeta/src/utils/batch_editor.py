"""
批量编辑工具 - 批量处理多个音频文件
"""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed

from ..core.audio_loader import AudioLoader
from ..core.metadata import AudioMetadata, MetadataField


@dataclass
class BatchOperation:
    """批量操作"""
    field: MetadataField
    value: Any
    operation: str  # 'set', 'replace', 'append', 'remove'


@dataclass
class BatchJob:
    """批量作业"""
    files: List[str]
    operations: List[BatchOperation]
    backup: bool = True


class BatchEditor:
    """批量编辑器"""
    
    def __init__(self):
        self.audio_loader = AudioLoader()
        self.progress_callback: Optional[Callable] = None
        self.error_callback: Optional[Callable] = None
    
    def create_job(
        self,
        files: List[str],
        operations: List[BatchOperation],
        backup: bool = True
    ) -> BatchJob:
        """创建批量作业"""
        return BatchJob(files=files, operations=operations, backup=backup)
    
    def execute(self, job: BatchJob) -> Dict[str, Any]:
        """执行批量作业"""
        results = {
            'total': len(job.files),
            'success': 0,
            'failed': 0,
            'errors': [],
        }
        
        for i, file_path in enumerate(job.files):
            try:
                # 创建备份
                if job.backup:
                    self._create_backup(file_path)
                
                # 加载元数据
                metadata = self.audio_loader.load(file_path)
                
                # 应用操作
                for operation in job.operations:
                    self._apply_operation(metadata, operation)
                
                # 保存元数据
                self.audio_loader.save(metadata)
                
                results['success'] += 1
                
            except Exception as e:
                results['failed'] += 1
                results['errors'].append({
                    'file': file_path,
                    'error': str(e)
                })
                
                if self.error_callback:
                    self.error_callback(file_path, str(e))
            
            # 更新进度
            if self.progress_callback:
                self.progress_callback(i + 1, len(job.files))
        
        return results
    
    def execute_parallel(self, job: BatchJob, max_workers: int = 4) -> Dict[str, Any]:
        """并行执行批量作业"""
        results = {
            'total': len(job.files),
            'success': 0,
            'failed': 0,
            'errors': [],
        }
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self._process_file, file_path, job.operations, job.backup): file_path
                for file_path in job.files
            }
            
            for i, future in enumerate(as_completed(futures)):
                file_path = futures[future]
                
                try:
                    success, error = future.result()
                    
                    if success:
                        results['success'] += 1
                    else:
                        results['failed'] += 1
                        results['errors'].append({
                            'file': file_path,
                            'error': error
                        })
                        
                        if self.error_callback:
                            self.error_callback(file_path, error)
                
                except Exception as e:
                    results['failed'] += 1
                    results['errors'].append({
                        'file': file_path,
                        'error': str(e)
                    })
                
                # 更新进度
                if self.progress_callback:
                    self.progress_callback(i + 1, len(job.files))
        
        return results
    
    def _process_file(self, file_path: str, operations: List[BatchOperation], backup: bool):
        """处理单个文件"""
        try:
            # 创建备份
            if backup:
                self._create_backup(file_path)
            
            # 加载元数据
            metadata = self.audio_loader.load(file_path)
            
            # 应用操作
            for operation in operations:
                self._apply_operation(metadata, operation)
            
            # 保存元数据
            self.audio_loader.save(metadata)
            
            return True, None
            
        except Exception as e:
            return False, str(e)
    
    def _apply_operation(self, metadata: AudioMetadata, operation: BatchOperation):
        """应用单个操作"""
        if operation.operation == 'set':
            metadata.set_field(operation.field, operation.value)
        
        elif operation.operation == 'replace':
            current_value = metadata.get_field(operation.field)
            if current_value and isinstance(current_value, str):
                new_value = current_value.replace(str(operation.value[0]), str(operation.value[1]))
                metadata.set_field(operation.field, new_value)
        
        elif operation.operation == 'append':
            current_value = metadata.get_field(operation.field)
            if current_value:
                new_value = f"{current_value}{operation.value}"
            else:
                new_value = operation.value
            metadata.set_field(operation.field, new_value)
        
        elif operation.operation == 'remove':
            metadata.set_field(operation.field, None)
    
    def _create_backup(self, file_path: str):
        """创建文件备份"""
        # 简单实现：复制文件
        backup_path = file_path + ".backup"
        
        try:
            import shutil
            shutil.copy2(file_path, backup_path)
        except Exception as e:
            print(f"创建备份失败：{e}")
    
    def find_and_replace(
        self,
        files: List[str],
        field: MetadataField,
        search: str,
        replace: str
    ) -> Dict[str, Any]:
        """查找并替换"""
        operation = BatchOperation(
            field=field,
            value=(search, replace),
            operation='replace'
        )
        
        job = BatchJob(files=files, operations=[operation])
        return self.execute(job)
    
    def copy_metadata(
        self,
        source_file: str,
        target_files: List[str],
        fields: Optional[List[MetadataField]] = None
    ) -> Dict[str, Any]:
        """从源文件复制元数据到目标文件"""
        # 加载源文件元数据
        source_metadata = self.audio_loader.load(source_file)
        
        operations = []
        
        if fields is None:
            fields = list(MetadataField)
        
        for field in fields:
            value = source_metadata.get_field(field)
            if value is not None:
                operations.append(BatchOperation(
                    field=field,
                    value=value,
                    operation='set'
                ))
        
        job = BatchJob(files=target_files, operations=operations)
        return self.execute(job)
    
    def auto_tag_from_filename(
        self,
        files: List[str],
        pattern: str = "{artist} - {title}"
    ) -> Dict[str, Any]:
        """从文件名自动标记"""
        operations_list = []
        
        for file_path in files:
            filename = Path(file_path).stem
            
            # 简单解析：假设格式为 "Artist - Title"
            if " - " in filename:
                parts = filename.split(" - ", 1)
                artist = parts[0].strip()
                title = parts[1].strip() if len(parts) > 1 else filename
                
                operations = [
                    BatchOperation(field=MetadataField.ARTIST, value=artist, operation='set'),
                    BatchOperation(field=MetadataField.TITLE, value=title, operation='set'),
                ]
                
                job = BatchJob(files=[file_path], operations=operations)
                self.execute(job)
        
        return {'status': 'completed'}
    
    def remove_tags(
        self,
        files: List[str],
        fields: Optional[List[MetadataField]] = None
    ) -> Dict[str, Any]:
        """删除标签"""
        if fields is None:
            fields = list(MetadataField)
        
        operations = [
            BatchOperation(field=field, value=None, operation='remove')
            for field in fields
        ]
        
        job = BatchJob(files=files, operations=operations)
        return self.execute(job)
    
    def generate_album_art(
        self,
        files: List[str],
        output_path: str,
        size: int = 1000
    ):
        """生成专辑封面缩略图"""
        from PIL import Image
        
        for file_path in files:
            try:
                metadata = self.audio_loader.load(file_path)
                
                if metadata.has_cover():
                    cover = metadata.cover_art
                    cover = cover.resize((size, size), Image.Resampling.LANCZOS)
                    cover.save(output_path, quality=95)
                    break  # 只取第一个有封面的文件
                    
            except Exception:
                continue
