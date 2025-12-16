# -*- coding: utf-8 -*-
"""
Parallel Processor for Large Files
Optimized for 20-70GB databases
"""

import os
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from typing import List, Callable, Any, Generator
import mmap


class ParallelProcessor:
    """Parallel file processing using all CPU cores"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.max_workers = config.get('max_workers') or multiprocessing.cpu_count()
        self.chunk_size = config.get('chunk_size', 1024 * 1024)  # 1MB default
    
    def get_cpu_count(self) -> int:
        """Get number of CPU cores"""
        return multiprocessing.cpu_count()
    
    def get_optimal_workers(self, file_count: int) -> int:
        """Calculate optimal number of workers"""
        cpu_count = multiprocessing.cpu_count()
        
        # For I/O bound tasks, we can use more threads than cores
        if file_count > cpu_count * 2:
            return cpu_count * 2
        elif file_count > cpu_count:
            return cpu_count
        else:
            return max(1, file_count)
    
    def process_files_parallel(self, files: List[str], processor_func: Callable) -> List[Any]:
        """Process list of files in parallel"""
        results = []
        optimal_workers = self.get_optimal_workers(len(files))
        
        with ThreadPoolExecutor(max_workers=optimal_workers) as executor:
            futures = {executor.submit(processor_func, f): f for f in files}
            
            for future in as_completed(futures):
                try:
                    result = future.result()
                    if result:
                        if isinstance(result, list):
                            results.extend(result)
                        else:
                            results.append(result)
                except Exception as e:
                    self.logger.error(f"Processing error: {e}")
        
        return results
    
    def read_file_chunks(self, file_path: str) -> Generator[bytes, None, None]:
        """Read file in chunks for memory efficiency"""
        try:
            with open(file_path, 'rb') as f:
                while True:
                    chunk = f.read(self.chunk_size)
                    if not chunk:
                        break
                    yield chunk
        except Exception as e:
            self.logger.error(f"Error reading {file_path}: {e}")
    
    def read_large_file_mmap(self, file_path: str) -> Generator[str, None, None]:
        """Read large file using memory mapping"""
        try:
            with open(file_path, 'rb') as f:
                # Check if file is not empty
                f.seek(0, 2)  # Go to end
                file_size = f.tell()
                
                if file_size == 0:
                    return
                
                f.seek(0)  # Go back to start
                
                with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                    for line in iter(mm.readline, b''):
                        yield line.decode('utf-8', errors='ignore').rstrip('\r\n')
        except Exception as e:
            self.logger.error(f"MMAP error {file_path}: {e}")
    
    def estimate_processing_time(self, total_size_bytes: int) -> float:
        """Estimate processing time based on file size"""
        # Approximate speed: 100 MB/sec per core
        speed_per_core = 100 * 1024 * 1024  # bytes/sec
        total_speed = speed_per_core * self.max_workers
        
        estimated_seconds = total_size_bytes / total_speed
        return estimated_seconds
    
    def format_time(self, seconds: float) -> str:
        """Format time for display"""
        if seconds < 60:
            return f"{seconds:.1f} sec"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f} min"
        else:
            hours = seconds / 3600
            return f"{hours:.1f} hours"
    
    def get_system_info(self) -> dict:
        """Get system information"""
        return {
            'cpu_count': multiprocessing.cpu_count(),
            'max_workers': self.max_workers,
            'chunk_size': self.chunk_size,
            'chunk_size_mb': self.chunk_size / (1024 * 1024)
        }
