# -*- coding: utf-8 -*-
"""
Advanced Configuration Manager with Themes
"""

import os
import json
import multiprocessing
from typing import Any, Dict, Optional


class ConfigManager:
    """Advanced program settings manager"""
    
    DEFAULT_CONFIG = {
        # Paths
        'database_path': 'bd',
        'results_path': 'results',
        'cache_path': 'cache',
        'logs_path': 'logs',
        
        # File settings
        'file_extensions': ['.txt', '.csv'],
        'encoding_priority': ['utf-8', 'cp1251', 'latin-1', 'cp866'],
        
        # Performance
        'max_workers': None,  # Auto = CPU count
        'use_mmap_threshold': 104857600,  # 100MB
        'chunk_size': 1048576,  # 1MB
        
        # Limits
        'max_results_per_file': 1000,
        'max_total_results': 10000,
        
        # Cache
        'cache_enabled': True,
        'cache_ttl': 3600,  # 1 hour
        
        # UI
        'theme': 'default',
        'show_progress': True,
        'color_output': True,
        
        # Export
        'export_format': 'txt',
        
        # Logging
        'log_level': 'INFO',
    }
    
    THEMES = ['default', 'hacker', 'ocean', 'fire', 'purple']
    
    def __init__(self, config_file: str = 'config.json'):
        self.config_file = config_file
        self.config = self.DEFAULT_CONFIG.copy()
        self._load_config()
        self._ensure_directories()
    
    def _load_config(self):
        """Load configuration from file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    self.config.update(loaded)
            except Exception as e:
                print(f"[!] Config load error: {e}")
        else:
            self._save_config()
    
    def _save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"[!] Config save error: {e}")
    
    def _ensure_directories(self):
        """Create necessary directories"""
        dirs = [
            self.config['database_path'],
            self.config['results_path'],
            self.config['cache_path'],
            self.config['logs_path'],
        ]
        for d in dirs:
            os.makedirs(d, exist_ok=True)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set configuration value"""
        self.config[key] = value
        self._save_config()
    
    def get_all(self) -> Dict:
        """Get all configuration"""
        return self.config.copy()
    
    def interactive_settings(self, ui):
        """Interactive settings menu with beautiful UI"""
        while True:
            cpu_count = multiprocessing.cpu_count()
            workers = self.config['max_workers'] or cpu_count
            
            print("\n" + "=" * 60)
            print("                    SETTINGS")
            print("=" * 60)
            print(f"""
  [1] Database path:      {self.config['database_path']}
  [2] Results path:       {self.config['results_path']}
  [3] Max workers:        {workers} (CPU cores: {cpu_count})
  [4] Cache:              {'ON' if self.config['cache_enabled'] else 'OFF'}
  [5] Cache TTL:          {self.config['cache_ttl']} sec
  [6] Export format:      {self.config['export_format']}
  [7] Theme:              {self.config['theme']}
  [8] Max results/file:   {self.config['max_results_per_file']}
  [9] Max total results:  {self.config['max_total_results']}
  
  [R] Reset to defaults
  [0] Back to menu
""")
            print("=" * 60)
            
            choice = input("\nSelect setting to change: ").strip().lower()
            
            if choice == '1':
                new_path = input("New database path: ").strip()
                if new_path:
                    self.set('database_path', new_path)
                    os.makedirs(new_path, exist_ok=True)
                    print(f"[OK] Path changed to: {new_path}")
                    
            elif choice == '2':
                new_path = input("New results path: ").strip()
                if new_path:
                    self.set('results_path', new_path)
                    os.makedirs(new_path, exist_ok=True)
                    print(f"[OK] Path changed to: {new_path}")
                    
            elif choice == '3':
                print(f"Current: {workers} | Available CPU cores: {cpu_count}")
                workers_input = input("Number of threads (Enter for auto): ").strip()
                if workers_input:
                    try:
                        new_workers = int(workers_input)
                        if 1 <= new_workers <= cpu_count * 2:
                            self.set('max_workers', new_workers)
                            print(f"[OK] Workers set to: {new_workers}")
                        else:
                            print(f"[!] Value must be between 1 and {cpu_count * 2}")
                    except ValueError:
                        print("[!] Enter a valid number")
                else:
                    self.set('max_workers', None)
                    print("[OK] Auto mode enabled")
                    
            elif choice == '4':
                self.set('cache_enabled', not self.config['cache_enabled'])
                status = 'ON' if self.config['cache_enabled'] else 'OFF'
                print(f"[OK] Cache: {status}")
                
            elif choice == '5':
                ttl = input("Cache TTL in seconds (default 3600): ").strip()
                if ttl:
                    try:
                        self.set('cache_ttl', int(ttl))
                        print(f"[OK] Cache TTL: {ttl} sec")
                    except:
                        print("[!] Enter a valid number")
                        
            elif choice == '6':
                print("Available formats: txt, csv, json")
                fmt = input("Export format: ").strip().lower()
                if fmt in ['txt', 'csv', 'json']:
                    self.set('export_format', fmt)
                    print(f"[OK] Format: {fmt}")
                else:
                    print("[!] Unknown format")
                    
            elif choice == '7':
                print(f"Available themes: {', '.join(self.THEMES)}")
                theme = input("Select theme: ").strip().lower()
                if theme in self.THEMES:
                    self.set('theme', theme)
                    print(f"[OK] Theme: {theme}")
                else:
                    print("[!] Unknown theme")
                    
            elif choice == '8':
                limit = input("Max results per file: ").strip()
                if limit:
                    try:
                        self.set('max_results_per_file', int(limit))
                        print(f"[OK] Limit set: {limit}")
                    except:
                        print("[!] Enter a valid number")
                        
            elif choice == '9':
                limit = input("Max total results: ").strip()
                if limit:
                    try:
                        self.set('max_total_results', int(limit))
                        print(f"[OK] Limit set: {limit}")
                    except:
                        print("[!] Enter a valid number")
                        
            elif choice == 'r':
                confirm = input("Reset all settings to defaults? (y/n): ").strip().lower()
                if confirm in ['y', 'yes']:
                    self.config = self.DEFAULT_CONFIG.copy()
                    self._save_config()
                    print("[OK] Settings reset to defaults")
                    
            elif choice == '0':
                break
            
            else:
                print("[!] Invalid choice")
