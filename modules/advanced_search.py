# -*- coding: utf-8 -*-
"""
Advanced Search Module with Filters and Regex Support
"""
import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
@dataclass
class SearchFilter:
    """Search filter configuration"""
    field: str = None           # Field to search (phone, email, etc.)
    exact_match: bool = False   # Exact match only
    case_sensitive: bool = False
    regex: bool = False         # Use regex
    exclude: List[str] = None   # Exclude patterns
    date_from: str = None
    date_to: str = None
    min_results: int = 0
    max_results: int = 10000
class AdvancedSearch:
    """Advanced search with filters, regex, and smart matching"""
    
    # Predefined patterns for common data types
    PATTERNS = {
        'telegram_id': r'\b(\d{6,12})\b',
        'phone_ru': r'(?:\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}',
        'phone_any': r'[\+]?\d{10,15}',
        'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        'username': r'@[a-zA-Z0-9_]{3,32}',
        'ip_address': r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
        'password': r'(?<=:)[^\s:]{6,50}(?=\s|$|:)',
        'name_ru': r'[А-ЯЁ][а-яё]+\s+[А-ЯЁ][а-яё]+(?:\s+[А-ЯЁ][а-яё]+)?',
        'name_en': r'[A-Z][a-z]+\s+[A-Z][a-z]+',
        'date': r'\b\d{2}[\.\/\-]\d{2}[\.\/\-]\d{2,4}\b',
        'url': r'https?://[^\s<>"{}|\\^`\[\]]+',
        'hash_md5': r'\b[a-fA-F0-9]{32}\b',
        'hash_sha1': r'\b[a-fA-F0-9]{40}\b',
        'credit_card': r'\b(?:\d{4}[\s\-]?){3}\d{4}\b',
        'passport_ru': r'\b\d{4}\s?\d{6}\b',
        'snils': r'\b\d{3}[\s\-]?\d{3}[\s\-]?\d{3}[\s\-]?\d{2}\b',
        'inn': r'\b\d{10,12}\b',
        'vk_id': r'(?:vk\.com/|id)(\d+)',
    }
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.last_search_stats = {}
    
    def parse_query(self, query: str) -> Dict[str, Any]:
        """Parse query and detect type"""
        query = query.strip()
        detected = {
            'original': query,
            'type': 'unknown',
            'normalized': query,
            'patterns': []
        }
        
        # Detect query type
        for name, pattern in self.PATTERNS.items():
            if re.search(pattern, query, re.IGNORECASE):
                detected['patterns'].append(name)
        
        # Primary type detection
        if re.match(r'^\d{6,12}$', query):
            detected['type'] = 'telegram_id'
        elif re.match(r'^[\+]?[78]?\d{10,11}$', query.replace(' ', '').replace('-', '')):
            detected['type'] = 'phone'
            detected['normalized'] = self._normalize_phone(query)
        elif '@' in query and '.' in query:
            detected['type'] = 'email'
            detected['normalized'] = query.lower()
        elif query.startswith('@'):
            detected['type'] = 'username'
            detected['normalized'] = query.lower()
        elif re.match(r'^[А-ЯЁ][а-яё]+\s+[А-ЯЁ][а-яё]+', query):
            detected['type'] = 'name_ru'
        elif re.match(r'^[A-Z][a-z]+\s+[A-Z][a-z]+', query):
            detected['type'] = 'name_en'
        
        return detected
    
    def _normalize_phone(self, phone: str) -> str:
        """Normalize phone number"""
        digits = re.sub(r'\D', '', phone)
        if len(digits) == 11 and digits[0] in '78':
            digits = '7' + digits[1:]
        return digits
    
    def build_search_pattern(self, query: str, filter: SearchFilter = None) -> str:
        """Build regex pattern for search"""
        if filter and filter.regex:
            return query
        
        # Escape special regex characters
        escaped = re.escape(query)
        
        if filter and filter.exact_match:
            return f'^{escaped}$'
        
        return escaped
    
    def match_line(self, line: str, query: str, filter: SearchFilter = None) -> Optional[Dict]:
        """Check if line matches query with optional filtering"""
        if filter and filter.case_sensitive:
            search_line = line
            search_query = query
        else:
            search_line = line.lower()
            search_query = query.lower()
        
        # Basic match
        if search_query not in search_line:
            return None
        
        # Exclude patterns
        if filter and filter.exclude:
            for exclude in filter.exclude:
                if exclude.lower() in search_line:
                    return None
        
        # Extract matched data
        match_info = {
            'matched': True,
            'line': line,
            'position': search_line.find(search_query),
            'extracted': self._extract_data(line)
        }
        
        return match_info
    
    def _extract_data(self, line: str) -> Dict[str, Any]:
        """Extract structured data from line"""
        extracted = {}
        
        for name, pattern in self.PATTERNS.items():
            matches = re.findall(pattern, line, re.IGNORECASE)
            if matches:
                if len(matches) == 1:
                    extracted[name] = matches[0]
                else:
                    extracted[name] = matches
        
        return extracted
    
    def filter_results(self, results: List[Dict], filter: SearchFilter) -> List[Dict]:
        """Apply additional filters to results"""
        if not filter:
            return results
        
        filtered = results
        
        # Filter by field
        if filter.field:
            filtered = [
                r for r in filtered 
                if filter.field in r.get('parsed', {}) or 
                   filter.field in r.get('extracted', {})
            ]
        
        # Limit results
        if filter.max_results:
            filtered = filtered[:filter.max_results]
        
        return filtered
    
    def get_search_suggestions(self, partial: str) -> List[str]:
        """Get search suggestions based on partial input"""
        suggestions = []
        
        # Phone patterns
        if partial.startswith('+7') or partial.startswith('8'):
            suggestions.append(f"{partial}XXXXXXXXXX"[:12])
        
        # Email patterns
        if '@' in partial and '.' not in partial.split('@')[-1]:
            domain = partial.split('@')[-1]
            for d in ['gmail.com', 'mail.ru', 'yandex.ru', 'icloud.com']:
                if d.startswith(domain):
                    suggestions.append(partial.split('@')[0] + '@' + d)
        
        return suggestions[:5]
    
    def highlight_match(self, line: str, query: str) -> str:
        """Highlight matched text in line"""
        if not query:
            return line
        
        pattern = re.compile(re.escape(query), re.IGNORECASE)
        return pattern.sub(f'**{query.upper()}**', line)
