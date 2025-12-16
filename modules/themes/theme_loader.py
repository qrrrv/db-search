# -*- coding: utf-8 -*-
"""
Theme Loader - Loads and manages themes
"""

import os
import sys
import time

try:
    from rich.console import Console
    from rich.text import Text
    from rich.panel import Panel
    from rich.align import Align
    from rich.table import Table
    from rich.box import ROUNDED
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


class AnimatedTheme:
    """Base class for themes"""
    
    def __init__(self, name, config):
        self.name = name
        self.config = config
        self.display_name = config.get('display_name', name.title())
        self.primary = config.get('primary', 'cyan')
        self.secondary = config.get('secondary', 'yellow')
        self.success = config.get('success', 'green')
        self.error = config.get('error', 'red')
        self.info = config.get('info', 'blue')
        self.dim = config.get('dim', 'bright_black')
        self.gradient = config.get('gradient', ['cyan'])
        self.banner_font = config.get('banner_font', 'slant')
        self.banner_text = config.get('banner_text', 'DB SEARCH')
        
        if RICH_AVAILABLE:
            self.console = Console()


class ThemeLoader:
    """Loads and manages all themes"""
    
    # All 15 themes with unique banners
    THEMES = {
        'default': {
            'display_name': 'Default (Cyan Wave)',
            'primary': 'cyan',
            'secondary': 'yellow',
            'success': 'green',
            'error': 'red',
            'info': 'blue',
            'dim': 'bright_black',
            'gradient': ['cyan', 'bright_cyan', 'white', 'bright_cyan', 'cyan'],
            'banner_font': 'slant',
            'banner_text': 'DB SEARCH'
        },
        
        'hacker': {
            'display_name': 'Hacker (Matrix Rain)',
            'primary': 'green',
            'secondary': 'bright_green',
            'success': 'green',
            'error': 'red',
            'info': 'green',
            'dim': 'dark_green',
            'gradient': ['green', 'bright_green', 'white', 'bright_green', 'green'],
            'banner_font': 'banner3',
            'banner_text': 'MATRIX DB'
        },
        
        'ocean': {
            'display_name': 'Ocean (Deep Waves)',
            'primary': 'blue',
            'secondary': 'cyan',
            'success': 'bright_cyan',
            'error': 'red',
            'info': 'bright_blue',
            'dim': 'bright_black',
            'gradient': ['blue', 'bright_blue', 'cyan', 'bright_cyan', 'white'],
            'banner_font': 'standard',
            'banner_text': 'OCEAN DB'
        },
        
        'fire': {
            'display_name': 'Fire (Burning Flames)',
            'primary': 'red',
            'secondary': 'yellow',
            'success': 'bright_yellow',
            'error': 'bright_red',
            'info': 'yellow',
            'dim': 'bright_black',
            'gradient': ['red', 'bright_red', 'yellow', 'bright_yellow', 'white'],
            'banner_font': 'doom',
            'banner_text': 'FIRE DB'
        },
        
        'purple': {
            'display_name': 'Purple (Dream Swirl)',
            'primary': 'magenta',
            'secondary': 'bright_magenta',
            'success': 'green',
            'error': 'red',
            'info': 'purple',
            'dim': 'bright_black',
            'gradient': ['magenta', 'bright_magenta', 'purple', 'bright_magenta', 'white'],
            'banner_font': 'big',
            'banner_text': 'PURPLE'
        },
        
        'cyberpunk': {
            'display_name': 'Cyberpunk 2077',
            'primary': 'bright_magenta',
            'secondary': 'bright_cyan',
            'success': 'bright_green',
            'error': 'bright_red',
            'info': 'cyan',
            'dim': 'bright_black',
            'gradient': ['magenta', 'cyan', 'yellow', 'bright_magenta'],
            'banner_font': 'banner3-D',
            'banner_text': 'CYBER DB'
        },
        
        'neon': {
            'display_name': 'Neon Lights',
            'primary': 'bright_green',
            'secondary': 'bright_magenta',
            'success': 'bright_cyan',
            'error': 'bright_red',
            'info': 'bright_blue',
            'dim': 'bright_black',
            'gradient': ['bright_green', 'bright_cyan', 'bright_magenta', 'bright_yellow', 'white'],
            'banner_font': 'digital',
            'banner_text': 'NEON DB'
        },
        
        'sunset': {
            'display_name': 'Sunset Vibes',
            'primary': 'yellow',
            'secondary': 'bright_red',
            'success': 'bright_yellow',
            'error': 'red',
            'info': 'yellow',
            'dim': 'bright_black',
            'gradient': ['yellow', 'bright_yellow', 'bright_red', 'magenta', 'bright_magenta'],
            'banner_font': 'bubble',
            'banner_text': 'SUNSET'
        },
        
        'arctic': {
            'display_name': 'Arctic Frost',
            'primary': 'bright_white',
            'secondary': 'bright_cyan',
            'success': 'bright_blue',
            'error': 'red',
            'info': 'cyan',
            'dim': 'bright_black',
            'gradient': ['white', 'bright_white', 'bright_cyan', 'cyan', 'bright_blue'],
            'banner_font': 'block',
            'banner_text': 'ARCTIC'
        },
        
        'dracula': {
            'display_name': 'Dracula Dark',
            'primary': 'purple',
            'secondary': 'bright_magenta',
            'success': 'bright_green',
            'error': 'bright_red',
            'info': 'cyan',
            'dim': 'bright_black',
            'gradient': ['purple', 'magenta', 'bright_magenta', 'red', 'bright_red'],
            'banner_font': 'shadow',
            'banner_text': 'DRACULA'
        },
        
        'retro': {
            'display_name': 'Retro 80s',
            'primary': 'bright_magenta',
            'secondary': 'bright_cyan',
            'success': 'bright_green',
            'error': 'bright_red',
            'info': 'bright_blue',
            'dim': 'bright_black',
            'gradient': ['bright_magenta', 'magenta', 'bright_cyan', 'cyan', 'bright_blue'],
            'banner_font': 'larry3d',
            'banner_text': 'RETRO'
        },
        
        'forest': {
            'display_name': 'Forest Nature',
            'primary': 'green',
            'secondary': 'bright_green',
            'success': 'bright_green',
            'error': 'red',
            'info': 'green',
            'dim': 'bright_black',
            'gradient': ['green', 'bright_green', 'yellow', 'bright_yellow', 'white'],
            'banner_font': 'banner',
            'banner_text': 'FOREST'
        },
        
        'galaxy': {
            'display_name': 'Galaxy Space',
            'primary': 'bright_blue',
            'secondary': 'bright_magenta',
            'success': 'bright_cyan',
            'error': 'bright_red',
            'info': 'purple',
            'dim': 'bright_black',
            'gradient': ['blue', 'bright_blue', 'purple', 'magenta', 'bright_white'],
            'banner_font': 'starwars',
            'banner_text': 'GALAXY'
        },
        
        'minimal': {
            'display_name': 'Minimal',
            'primary': 'white',
            'secondary': 'bright_white',
            'success': 'green',
            'error': 'red',
            'info': 'blue',
            'dim': 'bright_black',
            'gradient': ['white', 'bright_white'],
            'banner_font': 'small',
            'banner_text': 'MINIMAL DB'
        },
        
        'blood': {
            'display_name': 'Blood Moon',
            'primary': 'red',
            'secondary': 'bright_red',
            'success': 'bright_red',
            'error': 'bright_red',
            'info': 'red',
            'dim': 'bright_black',
            'gradient': ['red', 'bright_red', 'white', 'bright_red', 'red'],
            'banner_font': 'graffiti',
            'banner_text': 'BLOOD'
        },
        
        'gold': {
            'display_name': 'Gold Luxury',
            'primary': 'yellow',
            'secondary': 'bright_yellow',
            'success': 'bright_green',
            'error': 'red',
            'info': 'yellow',
            'dim': 'bright_black',
            'gradient': ['yellow', 'bright_yellow', 'white', 'bright_yellow', 'yellow'],
            'banner_font': 'epic',
            'banner_text': 'GOLD'
        },
    }
    
    def __init__(self):
        self.current_theme_name = 'default'
        self.themes = {}
        self._load_all_themes()
        
        if RICH_AVAILABLE:
            self.console = Console()
    
    def _load_all_themes(self):
        """Load all theme configurations"""
        for name, config in self.THEMES.items():
            self.themes[name] = AnimatedTheme(name, config)
    
    def get_theme(self, name=None):
        """Get theme by name"""
        name = name or self.current_theme_name
        return self.themes.get(name, self.themes['default'])
    
    def set_theme(self, name):
        """Set current theme"""
        if name in self.themes:
            self.current_theme_name = name
            return True
        return False
    
    def get_current_theme(self):
        """Get current theme"""
        return self.themes.get(self.current_theme_name, self.themes['default'])
    
    def list_themes(self):
        """List all themes with current marker"""
        return [(name, config['display_name'], name == self.current_theme_name) 
                for name, config in self.THEMES.items()]
    
    def show_theme_selector(self):
        """Show theme selector"""
        if not RICH_AVAILABLE:
            return self._simple_theme_selector()
        
        theme = self.get_current_theme()
        
        # Build theme list with current marker
        table = Table(
            title="SELECT THEME",
            box=ROUNDED,
            border_style=theme.primary,
            title_style=f"bold {theme.secondary}"
        )
        
        table.add_column("#", style="dim", width=4)
        table.add_column("Theme", width=12)
        table.add_column("Name", width=20)
        table.add_column("Preview", width=25)
        table.add_column("", width=3)  # Current marker
        
        for i, (name, display_name, is_current) in enumerate(self.list_themes(), 1):
            t = self.themes[name]
            
            # Create color preview
            preview = Text()
            for color in t.gradient[:5]:
                preview.append("***", style=f"bold {color}")
            
            # Current theme marker
            marker = "[*]" if is_current else ""
            marker_style = f"bold {theme.success}" if is_current else ""
            
            row_style = f"bold {theme.primary}" if is_current else ""
            
            table.add_row(
                str(i),
                name,
                display_name,
                preview,
                Text(marker, style=marker_style)
            )
        
        self.console.print()
        self.console.print(table)
        self.console.print()
        
        # Show current theme
        current = self.get_current_theme()
        self.console.print(f"[{theme.info}]Current theme: [{theme.success}]{current.display_name}[/][/]")
        
        # Get user choice
        self.console.print(f"\n[{theme.primary}]Enter theme number (or 0 to cancel): [/]", end="")
        
        try:
            choice = input().strip()
            if choice == '0' or not choice:
                return self.current_theme_name
            
            idx = int(choice) - 1
            theme_names = list(self.THEMES.keys())
            
            if 0 <= idx < len(theme_names):
                new_theme = theme_names[idx]
                self.set_theme(new_theme)
                
                # Show confirmation
                self.console.print()
                new = self.get_current_theme()
                
                styled = Text()
                msg = f"Theme changed to: {new.display_name}"
                for i, char in enumerate(msg):
                    color = new.gradient[i % len(new.gradient)]
                    styled.append(char, style=f"bold {color}")
                
                self.console.print(Panel(Align.center(styled), border_style=new.primary))
                
                return new_theme
        except:
            pass
        
        return self.current_theme_name
    
    def _simple_theme_selector(self):
        """Simple theme selector without Rich"""
        print("\n" + "=" * 50)
        print("  SELECT THEME")
        print("=" * 50)
        
        for i, (name, display_name, is_current) in enumerate(self.list_themes(), 1):
            marker = " [*]" if is_current else ""
            print(f"  [{i}] {name} - {display_name}{marker}")
        
        print()
        choice = input("Enter theme number: ").strip()
        
        try:
            idx = int(choice) - 1
            theme_names = list(self.THEMES.keys())
            if 0 <= idx < len(theme_names):
                self.set_theme(theme_names[idx])
                return theme_names[idx]
        except:
            pass
        
        return self.current_theme_name