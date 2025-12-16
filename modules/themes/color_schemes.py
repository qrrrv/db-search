# -*- coding: utf-8 -*-
"""
Color Schemes - Beautiful color palettes for themes
"""


class ColorSchemes:
    """Collection of beautiful color schemes"""
    
    SCHEMES = {
        # Classic Themes
        'default': {
            'name': 'Default',
            'primary': 'cyan',
            'secondary': 'yellow',
            'success': 'green',
            'error': 'red',
            'warning': 'yellow',
            'info': 'blue',
            'accent': 'magenta',
            'dim': 'bright_black',
            'bg': 'default',
            'gradient': ['cyan', 'bright_cyan', 'white'],
            'banner_style': 'slant'
        },
        
        'hacker': {
            'name': 'Hacker (Matrix)',
            'primary': 'green',
            'secondary': 'bright_green',
            'success': 'green',
            'error': 'red',
            'warning': 'yellow',
            'info': 'green',
            'accent': 'bright_green',
            'dim': 'dark_green',
            'bg': 'black',
            'gradient': ['green', 'bright_green', 'white'],
            'banner_style': 'doom'
        },
        
        'ocean': {
            'name': 'Ocean',
            'primary': 'blue',
            'secondary': 'cyan',
            'success': 'bright_cyan',
            'error': 'red',
            'warning': 'yellow',
            'info': 'bright_blue',
            'accent': 'cyan',
            'dim': 'bright_black',
            'bg': 'default',
            'gradient': ['blue', 'cyan', 'bright_cyan', 'white'],
            'banner_style': 'banner3'
        },
        
        'fire': {
            'name': 'Fire',
            'primary': 'red',
            'secondary': 'yellow',
            'success': 'bright_yellow',
            'error': 'bright_red',
            'warning': 'orange3',
            'info': 'yellow',
            'accent': 'bright_red',
            'dim': 'dark_red',
            'bg': 'default',
            'gradient': ['red', 'bright_red', 'yellow', 'bright_yellow'],
            'banner_style': 'fire_font-s'
        },
        
        'purple': {
            'name': 'Purple Dreams',
            'primary': 'magenta',
            'secondary': 'bright_magenta',
            'success': 'green',
            'error': 'red',
            'warning': 'yellow',
            'info': 'purple',
            'accent': 'bright_magenta',
            'dim': 'bright_black',
            'bg': 'default',
            'gradient': ['magenta', 'bright_magenta', 'purple', 'white'],
            'banner_style': 'epic'
        },
        
        # New Beautiful Themes
        'cyberpunk': {
            'name': 'Cyberpunk 2077',
            'primary': 'bright_magenta',
            'secondary': 'bright_cyan',
            'success': 'bright_green',
            'error': 'bright_red',
            'warning': 'bright_yellow',
            'info': 'cyan',
            'accent': 'yellow',
            'dim': 'bright_black',
            'bg': 'default',
            'gradient': ['magenta', 'cyan', 'yellow', 'bright_magenta'],
            'banner_style': 'cyberlarge'
        },
        
        'neon': {
            'name': 'Neon Lights',
            'primary': 'bright_green',
            'secondary': 'bright_magenta',
            'success': 'bright_cyan',
            'error': 'bright_red',
            'warning': 'bright_yellow',
            'info': 'bright_blue',
            'accent': 'bright_white',
            'dim': 'bright_black',
            'bg': 'default',
            'gradient': ['bright_green', 'bright_cyan', 'bright_magenta', 'bright_yellow'],
            'banner_style': 'electronic'
        },
        
        'sunset': {
            'name': 'Sunset',
            'primary': 'orange3',
            'secondary': 'bright_red',
            'success': 'bright_yellow',
            'error': 'red',
            'warning': 'yellow',
            'info': 'orange1',
            'accent': 'magenta',
            'dim': 'bright_black',
            'bg': 'default',
            'gradient': ['yellow', 'orange3', 'bright_red', 'magenta'],
            'banner_style': 'sunset'
        },
        
        'arctic': {
            'name': 'Arctic',
            'primary': 'bright_white',
            'secondary': 'bright_cyan',
            'success': 'bright_blue',
            'error': 'red',
            'warning': 'yellow',
            'info': 'cyan',
            'accent': 'bright_white',
            'dim': 'bright_black',
            'bg': 'default',
            'gradient': ['white', 'bright_cyan', 'cyan', 'bright_blue'],
            'banner_style': 'banner'
        },
        
        'dracula': {
            'name': 'Dracula',
            'primary': 'purple',
            'secondary': 'bright_magenta',
            'success': 'bright_green',
            'error': 'bright_red',
            'warning': 'bright_yellow',
            'info': 'cyan',
            'accent': 'magenta',
            'dim': 'bright_black',
            'bg': 'default',
            'gradient': ['purple', 'magenta', 'bright_magenta', 'cyan'],
            'banner_style': 'bloody'
        },
        
        'retro': {
            'name': 'Retro 80s',
            'primary': 'bright_magenta',
            'secondary': 'bright_cyan',
            'success': 'bright_green',
            'error': 'bright_red',
            'warning': 'bright_yellow',
            'info': 'bright_blue',
            'accent': 'bright_white',
            'dim': 'bright_black',
            'bg': 'default',
            'gradient': ['bright_magenta', 'bright_blue', 'bright_cyan'],
            'banner_style': 'univers'
        },
        
        'forest': {
            'name': 'Forest',
            'primary': 'green',
            'secondary': 'bright_green',
            'success': 'bright_green',
            'error': 'red',
            'warning': 'yellow',
            'info': 'green',
            'accent': 'bright_yellow',
            'dim': 'bright_black',
            'bg': 'default',
            'gradient': ['green', 'bright_green', 'yellow', 'bright_yellow'],
            'banner_style': 'trees'
        },
        
        'galaxy': {
            'name': 'Galaxy',
            'primary': 'bright_blue',
            'secondary': 'bright_magenta',
            'success': 'bright_cyan',
            'error': 'bright_red',
            'warning': 'bright_yellow',
            'info': 'purple',
            'accent': 'bright_white',
            'dim': 'bright_black',
            'bg': 'default',
            'gradient': ['blue', 'purple', 'magenta', 'bright_white'],
            'banner_style': 'starwars'
        },
        
        'minimal': {
            'name': 'Minimal',
            'primary': 'white',
            'secondary': 'bright_white',
            'success': 'green',
            'error': 'red',
            'warning': 'yellow',
            'info': 'blue',
            'accent': 'cyan',
            'dim': 'bright_black',
            'bg': 'default',
            'gradient': ['white', 'bright_white'],
            'banner_style': 'small'
        },
        
        'blood': {
            'name': 'Blood Moon',
            'primary': 'red',
            'secondary': 'bright_red',
            'success': 'bright_red',
            'error': 'bright_red',
            'warning': 'bright_yellow',
            'info': 'red',
            'accent': 'bright_white',
            'dim': 'bright_black',
            'bg': 'default',
            'gradient': ['red', 'bright_red', 'white'],
            'banner_style': 'poison'
        },
        
        'gold': {
            'name': 'Gold Luxury',
            'primary': 'yellow',
            'secondary': 'bright_yellow',
            'success': 'bright_green',
            'error': 'red',
            'warning': 'bright_yellow',
            'info': 'yellow',
            'accent': 'bright_white',
            'dim': 'bright_black',
            'bg': 'default',
            'gradient': ['yellow', 'bright_yellow', 'white'],
            'banner_style': 'colossal'
        },
    }
    
    @classmethod
    def get_scheme(cls, name: str) -> dict:
        """Get color scheme by name"""
        return cls.SCHEMES.get(name, cls.SCHEMES['default'])
    
    @classmethod
    def list_schemes(cls) -> list:
        """Get list of all scheme names"""
        return list(cls.SCHEMES.keys())
    
    @classmethod
    def get_scheme_preview(cls, name: str) -> str:
        """Get preview string for scheme"""
        scheme = cls.get_scheme(name)
        return f"{scheme['name']}: {scheme['primary']} / {scheme['secondary']} / {scheme['accent']}"