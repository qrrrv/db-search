# -*- coding: utf-8 -*-
"""
Advanced Search Engine with Multiple Search Modes
"""

import os
import re
import csv
import mmap
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any, Optional, Generator
import multiprocessing

try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False


class SearchEngine:
    """Powerful search engine for large databases"""
    
    def __init__(self, config, logger, cache, indexer, processor, db_manager):
        self.config = config
        self.logger = logger
        self.cache = cache
        self.indexer = indexer
        self.processor = processor
        self.db_manager = db_manager
        self.results = []
        self.total_lines_searched = 0
        self.files_searched = 0
        self.search_time = 0
    
    def search(self, query: str, search_mode: str = 'normal') -> List[Dict[str, Any]]:
        """Main search method"""
        start_time = time.time()
        self.results = []
        self.total_lines_searched = 0
        self.files_searched = 0
        
        query = query.strip()
        if not query:
            return []
        
        # Check cache
        cached = self.cache.get(query)
        if cached:
            self.logger.info(f"Cache hit for: {query}")
            self.search_time = time.time() - start_time
            return cached
        
        # Get database files
        db_path = self.config.get('database_path', 'bd')
        files = self._get_database_files(db_path)
        
        if not files:
            self.logger.warning("No database files found!")
            return []
        
        self.logger.info(f"Searching in {len(files)} files for: {query}")
        
        # Parallel search
        max_workers = self.config.get('max_workers') or multiprocessing.cpu_count()
        
        # Show progress
        if TQDM_AVAILABLE:
            with tqdm(total=len(files), desc="Searching", unit="file",
                     bar_format="{l_bar}{bar:30}{r_bar}",
                     colour='cyan') as pbar:
                
                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    futures = {
                        executor.submit(self._search_file, file_path, query, search_mode): file_path 
                        for file_path in files
                    }
                    
                    for future in as_completed(futures):
                        file_path = futures[future]
                        try:
                            file_results = future.result()
                            self.results.extend(file_results)
                            self.files_searched += 1
                            pbar.update(1)
                            pbar.set_postfix({'found': len(self.results)})
                        except Exception as e:
                            self.logger.error(f"Error searching {file_path}: {e}")
                            pbar.update(1)
        else:
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {
                    executor.submit(self._search_file, file_path, query, search_mode): file_path 
                    for file_path in files
                }
                
                for future in as_completed(futures):
                    file_path = futures[future]
                    try:
                        file_results = future.result()
                        self.results.extend(file_results)
                        self.files_searched += 1
                        print(f"\rSearched: {self.files_searched}/{len(files)} | Found: {len(self.results)}", end="")
                    except Exception as e:
                        self.logger.error(f"Error: {e}")
            print()
        
        # Limit results
        max_results = self.config.get('max_total_results', 10000)
        if len(self.results) > max_results:
            self.results = self.results[:max_results]
        
        # Save to cache
        if self.results:
            self.cache.set(query, self.results)
        
        self.search_time = time.time() - start_time
        self.logger.info(f"Search complete. Found: {len(self.results)} in {self.search_time:.2f}s")
        
        return self.results
    
    def _get_database_files(self, path: str) -> List[str]:
        """Get list of database files"""
        files = []
        extensions = self.config.get('file_extensions', ['.txt', '.csv'])
        
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
            return files
        
        for root, dirs, filenames in os.walk(path):
            for filename in filenames:
                if any(filename.lower().endswith(ext) for ext in extensions):
                    files.append(os.path.join(root, filename))
        
        return files
    
    def _search_file(self, file_path: str, query: str, mode: str = 'normal') -> List[Dict[str, Any]]:
        """Search in single file"""
        results = []
        query_lower = query.lower()
        query_bytes = query.lower().encode('utf-8', errors='ignore')
        
        try:
            file_size = os.path.getsize(file_path)
            use_mmap_threshold = self.config.get('use_mmap_threshold', 100 * 1024 * 1024)
            
            # Use mmap for large files (>100MB)
            if file_size > use_mmap_threshold:
                results = self._search_file_mmap(file_path, query_bytes, query_lower)
            else:
                results = self._search_file_standard(file_path, query_lower, mode)
                
        except Exception as e:
            self.logger.error(f"Error reading {file_path}: {e}")
        
        return results
    
    def _search_file_mmap(self, file_path: str, query_bytes: bytes, query_str: str) -> List[Dict[str, Any]]:
        """Memory-mapped search for large files"""
        results = []
        max_results = self.config.get('max_results_per_file', 1000)
        
        try:
            with open(file_path, 'rb') as f:
                with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                    line_num = 0
                    start = 0
                    
                    while True:
                        line_end = mm.find(b'\n', start)
                        if line_end == -1:
                            line = mm[start:]
                            if query_bytes in line.lower():
                                results.append(self._create_result(
                                    file_path, line_num, 
                                    line.decode('utf-8', errors='ignore').strip()
                                ))
                            break
                        
                        line = mm[start:line_end]
                        line_num += 1
                        self.total_lines_searched += 1
                        
                        if query_bytes in line.lower():
                            results.append(self._create_result(
                                file_path, line_num,
                                line.decode('utf-8', errors='ignore').strip()
                            ))
                        
                        start = line_end + 1
                        
                        if len(results) >= max_results:
                            break
                            
        except Exception as e:
            self.logger.error(f"MMAP error in {file_path}: {e}")
        
        return results
    
    def _search_file_standard(self, file_path: str, query: str, mode: str) -> List[Dict[str, Any]]:
        """Standard line-by-line search"""
        results = []
        encodings = self.config.get('encoding_priority', ['utf-8', 'cp1251', 'latin-1', 'cp866'])
        max_results = self.config.get('max_results_per_file', 1000)
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                    for line_num, line in enumerate(f, 1):
                        self.total_lines_searched += 1
                        
                        # Search based on mode
                        found = False
                        if mode == 'exact':
                            found = query == line.strip().lower()
                        elif mode == 'regex':
                            try:
                                found = bool(re.search(query, line, re.IGNORECASE))
                            except:
                                found = query in line.lower()
                        else:  # normal
                            found = query in line.lower()
                        
                        if found:
                            results.append(self._create_result(file_path, line_num, line.strip()))
                            
                            if len(results) >= max_results:
                                break
                break
            except UnicodeDecodeError:
                continue
            except Exception as e:
                self.logger.error(f"Error reading {file_path} ({encoding}): {e}")
                break
        
        return results
    
    def _create_result(self, file_path: str, line_num: int, line: str) -> Dict[str, Any]:
        """Create search result entry"""
        parsed_data = self._parse_line(line, file_path)
        
        return {
            'file': os.path.basename(file_path),
            'file_path': file_path,
            'line_number': line_num,
            'raw_data': line,
            'parsed': parsed_data
        }
    
    def _parse_line(self, line: str, file_path: str) -> Dict[str, Any]:
        """Parse data from line"""
        parsed = {}
        
        # Detect delimiter
        if file_path.endswith('.csv'):
            parts = line.split(',')
        elif ':' in line:
            parts = line.split(':')
        elif ';' in line:
            parts = line.split(';')
        elif '\t' in line:
            parts = line.split('\t')
        elif '|' in line:
            parts = line.split('|')
        else:
            parts = line.split()
        
        # Extract known fields
        for part in parts:
            part = part.strip()
            if not part:
                continue
            
            # Telegram ID (6-12 digits)
            if re.match(r'^\d{6,12}$', part) and 'telegram_id' not in parsed:
                parsed['telegram_id'] = part
            
            # Phone number
            elif re.match(r'^[\+]?[\d\s\-\(\)]{10,15}$', part.replace(' ', '')) and 'phone' not in parsed:
                parsed['phone'] = part
            
            # Email
            elif re.match(r'^[\w\.\-\+]+@[\w\.\-]+\.\w+$', part, re.IGNORECASE) and 'email' not in parsed:
                parsed['email'] = part
            
            # Username (@username)
            elif part.startswith('@') and len(part) > 1 and 'username' not in parsed:
                parsed['username'] = part
            
            # Name (cyrillic or latin letters only)
            elif re.match(r'^[A-Za-zА-Яа-яЁёІіЇїЄєҐґ]{2,}$', part):
                if 'first_name' not in parsed:
                    parsed['first_name'] = part
                elif 'last_name' not in parsed:
                    parsed['last_name'] = part
                elif 'patronymic' not in parsed:
                    parsed['patronymic'] = part
        
        return parsed
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get search statistics"""
        return {
            'total_results': len(self.results),
            'files_searched': self.files_searched,
            'lines_searched': self.total_lines_searched,
            'search_time': self.search_time
        }
    
    def search_by_field(self, field: str, value: str) -> List[Dict[str, Any]]:
        """Search by specific field (phone, email, etc.)"""
        all_results = self.search(value)
        
        # Filter by field
        filtered = [
            r for r in all_results 
            if r.get('parsed', {}).get(field, '').lower() == value.lower()
        ]
        
        return filtered if filtered else all_results
