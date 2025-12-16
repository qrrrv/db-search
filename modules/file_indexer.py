# -*- coding: utf-8 -*-
"""
File Indexer Module
"""

import os
import time
import json
import hashlib
from typing import Dict, List, Any

try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False

try:
    from alive_progress import alive_bar
    ALIVE_AVAILABLE = True
except ImportError:
    ALIVE_AVAILABLE = False


class FileIndexer:
    """File indexer for fast search"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.index = {}
        self.stats = {
            'files': 0,
            'records': 0,
            'time': 0,
            'total_size': 0
        }
        self.index_file = os.path.join(config.get('cache_path', 'cache'), 'index.json')
        self._load_index()
    
    def _load_index(self):
        """Load existing index"""
        if os.path.exists(self.index_file):
            try:
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    self.index = json.load(f)
                self.logger.info(f"Index loaded: {len(self.index)} files")
            except Exception as e:
                self.logger.error(f"Error loading index: {e}")
                self.index = {}
    
    def _save_index(self):
        """Save index"""
        try:
            os.makedirs(os.path.dirname(self.index_file), exist_ok=True)
            with open(self.index_file, 'w', encoding='utf-8') as f:
                json.dump(self.index, f, ensure_ascii=False, indent=2)
            self.logger.info("Index saved")
        except Exception as e:
            self.logger.error(f"Error saving index: {e}")
    
    def index_all_databases(self):
        """Index all databases"""
        start_time = time.time()
        db_path = self.config.get('database_path', 'bd')
        
        if not os.path.exists(db_path):
            os.makedirs(db_path, exist_ok=True)
            self.logger.warning(f"Created empty directory: {db_path}")
            print(f"\n[!] Folder '{db_path}' is empty. Add your databases there.")
            return
        
        files = self._get_all_files(db_path)
        self.stats['files'] = len(files)
        
        if not files:
            print(f"\n[!] No database files found in '{db_path}'")
            return
        
        print(f"\n[*] Found {len(files)} files for indexing\n")
        
        total_records = 0
        total_size = 0
        
        if ALIVE_AVAILABLE:
            with alive_bar(len(files), title='Indexing', bar='smooth', spinner='dots_waves') as bar:
                for file_path in files:
                    records = self._index_file(file_path)
                    total_records += records
                    try:
                        total_size += os.path.getsize(file_path)
                    except:
                        pass
                    bar()
        elif TQDM_AVAILABLE:
            with tqdm(total=len(files), desc="Indexing", unit="file",
                     bar_format="{l_bar}{bar:30}{r_bar}", colour='green') as pbar:
                for file_path in files:
                    records = self._index_file(file_path)
                    total_records += records
                    try:
                        total_size += os.path.getsize(file_path)
                    except:
                        pass
                    pbar.update(1)
                    pbar.set_postfix({'records': total_records})
        else:
            for i, file_path in enumerate(files, 1):
                records = self._index_file(file_path)
                total_records += records
                try:
                    total_size += os.path.getsize(file_path)
                except:
                    pass
                print(f"\r[{i}/{len(files)}] Indexed: {total_records} records", end="")
            print()
        
        self.stats['records'] = total_records
        self.stats['time'] = time.time() - start_time
        self.stats['total_size'] = total_size
        
        self._save_index()
        
        self.logger.info(
            f"Indexing complete: {self.stats['files']} files, "
            f"{self.stats['records']} records in {self.stats['time']:.2f} sec"
        )
    
    def _get_all_files(self, path):
        """Get list of all database files"""
        files = []
        extensions = self.config.get('file_extensions', ['.txt', '.csv'])
        
        for root, dirs, filenames in os.walk(path):
            for filename in filenames:
                if any(filename.lower().endswith(ext) for ext in extensions):
                    files.append(os.path.join(root, filename))
        
        return files
    
    def _index_file(self, file_path):
        """Index single file"""
        try:
            file_hash = self._get_file_hash(file_path)
            
            if file_path in self.index:
                if self.index[file_path].get('hash') == file_hash:
                    return self.index[file_path].get('lines', 0)
            
            lines = 0
            file_size = os.path.getsize(file_path)
            
            encodings = self.config.get('encoding_priority', ['utf-8', 'cp1251', 'latin-1'])
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                        lines = sum(1 for _ in f)
                    break
                except:
                    continue
            
            self.index[file_path] = {
                'hash': file_hash,
                'lines': lines,
                'size': file_size,
                'name': os.path.basename(file_path),
                'indexed_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return lines
            
        except Exception as e:
            self.logger.error(f"Error indexing {file_path}: {e}")
            return 0
    
    def _get_file_hash(self, file_path):
        """Get file hash"""
        try:
            stat = os.stat(file_path)
            return f"{stat.st_size}_{stat.st_mtime}"
        except:
            return ""
    
    def get_stats(self):
        """Get indexing statistics"""
        return self.stats.copy()
    
    def is_file_indexed(self, file_path):
        return file_path in self.index
    
    def get_indexed_files_count(self):
        return len(self.index)
    
    def clear_index(self):
        """Clear all index data"""
        self.index = {}
        if os.path.exists(self.index_file):
            os.remove(self.index_file)
        self.logger.info("Index cleared")