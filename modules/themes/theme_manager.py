# -*- coding: utf-8 -*-
"""
Theme Manager - Controls all visual aspects
"""

import os
import json
from typing import Dict, Any, Optional

try:
    from rich.console import Console
    from rich.theme import Theme as RichTheme
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

from .color_schemes import ColorSchemes


class ThemeManager:
    """Manages themes and visual customization"""
    
    def __init__(self, config_path: str = 'themes_config.json'):
        self.config_path = config_path
        self.current_theme = 'default'
        self.custom_themes = {}
        self.load_config()
    
    def load_config(self):
        """Load theme configuration"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.current_theme = data.get('current', 'default')
                    self.custom_themes = data.get('custom', {})
            except:
                pass
    
    def save_config(self):
        """Save theme configuration"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'current': self.current_theme,
                    'custom': self.custom_themes
                }, f, indent=2)
        except:
            pass
    
    def get_theme(self, name: str = None) -> dict:
        """Get theme by name or current theme"""
        name = name or self.current_theme
        
        # Check custom themes first
        if name in self.custom_themes:
            return self.custom_themes[name]
        
        # Then built-in schemes
        return ColorSchemes.get_scheme(name)
    
    def set_theme(self, name: str) -> bool:
        """Set current theme"""
        if name in ColorSchemes.list_schemes() or name in self.custom_themes:
            self.current_theme = name
            self.save_config()
            return True
        return False
    
    def get_color(self, color_type: str) -> str:
        """Get specific color from current theme"""
        theme = self.get_theme()
        return theme.get(color_type, 'white')
    
    def get_gradient(self) -> list:
        """Get gradient colors for current theme"""
        theme = self.get_theme()
        return theme.get('gradient', ['white'])
    
    def get_banner_style(self) -> str:
        """Get ASCII art font style for banner"""
        theme = self.get_theme()
        return theme.get('banner_style', 'slant')
    
    def list_themes(self) -> list:
        """List all available themes"""
        themes = ColorSchemes.list_schemes()
        themes.extend(self.custom_themes.keys())
        return themes
    
    def create_custom_theme(self, name: str, base: str = 'default', **overrides) -> bool:
        """Create a custom theme based on existing one"""
        base_theme = ColorSchemes.get_scheme(base).copy()
        base_theme.update(overrides)
        base_theme['name'] = name
        self.custom_themes[name] = base_theme
        self.save_config()
        return True
    
    def delete_custom_theme(self, name: str) -> bool:
        """Delete a custom theme"""
        if name in self.custom_themes:
            del self.custom_themes[name]
            self.save_config()
            return True
        return False
    
    def get_rich_theme(self) -> Optional['RichTheme']:
        """Get Rich library theme object"""
        if not RICH_AVAILABLE:
            return None
        
        theme = self.get_theme()
        return RichTheme({
            'primary': theme.get('primary', 'cyan'),
            'secondary': theme.get('secondary', 'yellow'),
            'success': theme.get('success', 'green'),
            'error': theme.get('error', 'red'),
            'warning': theme.get('warning', 'yellow'),
            'info': theme.get('info', 'blue'),
            'accent': theme.get('accent', 'magenta'),
            'dim': theme.get('dim', 'bright_black'),
        })
    
    def apply_to_console(self, console: 'Console') -> 'Console':
        """Apply theme to Rich console"""
        if RICH_AVAILABLE and console:
            rich_theme = self.get_rich_theme()
            if rich_theme:
                console._theme = rich_theme
        return console