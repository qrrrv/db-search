# -*- coding: utf-8 -*-
"""
Logger Module
"""

import os
import logging
from datetime import datetime


class Logger:
    """Logging manager"""
    
    def __init__(self, config):
        self.config = config
        self.log_path = config.get('logs_path', 'logs')
        self.log_level = config.get('log_level', 'INFO')
        
        os.makedirs(self.log_path, exist_ok=True)
        
        self.logger = logging.getLogger('DBSearch')
        self.logger.setLevel(getattr(logging, self.log_level, logging.INFO))
        self.logger.handlers = []
        
        log_file = os.path.join(
            self.log_path,
            f"search_{datetime.now().strftime('%Y%m%d')}.log"
        )
        
        try:
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            
            formatter = logging.Formatter(
                '%(asctime)s | %(levelname)-8s | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        except Exception as e:
            print(f"[!] Cannot create log file: {e}")
    
    def info(self, message):
        self.logger.info(message)
    
    def warning(self, message):
        self.logger.warning(message)
    
    def error(self, message):
        self.logger.error(message)
    
    def debug(self, message):
        self.logger.debug(message)
    
    def critical(self, message):
        self.logger.critical(message)
    
    def search_log(self, query, results_count, duration):
        self.info(f"SEARCH: '{query}' | Results: {results_count} | Time: {duration:.2f}s")
    
    def export_log(self, format_type, filepath, records):
        self.info(f"EXPORT: {format_type.upper()} | File: {filepath} | Records: {records}")