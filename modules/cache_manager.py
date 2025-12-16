# -*- coding: utf-8 -*-
"""
Advanced Cache Manager with Statistics
"""

import os
import json
import time
import hashlib
from typing import Any, Optional, Dict, List


class CacheManager:
    """Advanced caching for search results"""
    
    def __init__(self, config):
        self.config = config
        self.cache_path = config.get('cache_path', 'cache')
        self.cache_enabled = config.get('cache_enabled', True)
        self.cache_ttl = config.get('cache_ttl', 3600)  # 1 hour
        self.cache = {}
        self.hit_count = 0
        self.miss_count = 0
        
        os.makedirs(self.cache_path, exist_ok=True)
        self._load_cache()
    
    def _get_cache_file(self) -> str:
        """Get cache file path"""
        return os.path.join(self.cache_path, 'search_cache.json')
    
    def _load_cache(self):
        """Load cache from file"""
        cache_file = self._get_cache_file()
        
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.cache = data.get('cache', {})
                    self.hit_count = data.get('hit_count', 0)
                    self.miss_count = data.get('miss_count', 0)
                
                # Clean expired entries
                self._cleanup_expired()
            except:
                self.cache = {}
    
    def _save_cache(self):
        """Save cache to file"""
        try:
            data = {
                'cache': self.cache,
                'hit_count': self.hit_count,
                'miss_count': self.miss_count,
                'saved_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            with open(self._get_cache_file(), 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False)
        except:
            pass
    
    def _get_key(self, query: str) -> str:
        """Generate cache key"""
        return hashlib.md5(query.lower().strip().encode()).hexdigest()
    
    def get(self, query: str) -> Optional[List[Dict]]:
        """Get from cache"""
        if not self.cache_enabled:
            return None
        
        key = self._get_key(query)
        
        if key in self.cache:
            entry = self.cache[key]
            
            # Check TTL
            if time.time() - entry.get('timestamp', 0) < self.cache_ttl:
                self.hit_count += 1
                return entry.get('data')
            else:
                # Expired
                del self.cache[key]
        
        self.miss_count += 1
        return None
    
    def set(self, query: str, data: List[Dict]):
        """Save to cache"""
        if not self.cache_enabled:
            return
        
        key = self._get_key(query)
        
        self.cache[key] = {
            'query': query,
            'data': data[:1000],  # Limit size
            'timestamp': time.time(),
            'results_count': len(data)
        }
        
        self._save_cache()
    
    def _cleanup_expired(self):
        """Clean expired entries"""
        current_time = time.time()
        expired_keys = [
            key for key, entry in self.cache.items()
            if current_time - entry.get('timestamp', 0) >= self.cache_ttl
        ]
        
        for key in expired_keys:
            del self.cache[key]
        
        if expired_keys:
            self._save_cache()
    
    def clear(self):
        """Clear all cache"""
        self.cache = {}
        self.hit_count = 0
        self.miss_count = 0
        
        cache_file = self._get_cache_file()
        if os.path.exists(cache_file):
            os.remove(cache_file)
        
        # Clear other cache files
        for f in os.listdir(self.cache_path):
            filepath = os.path.join(self.cache_path, f)
            try:
                if os.path.isfile(filepath):
                    os.remove(filepath)
            except:
                pass
    
    def get_size(self) -> int:
        """Get cache size"""
        return len(self.cache)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total = self.hit_count + self.miss_count
        hit_rate = (self.hit_count / total * 100) if total > 0 else 0
        
        return {
            'entries': len(self.cache),
            'hits': self.hit_count,
            'misses': self.miss_count,
            'hit_rate': f"{hit_rate:.1f}%",
            'enabled': self.cache_enabled
        }
