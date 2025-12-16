# -*- coding: utf-8 -*-
"""
Display - Main display controller
"""

import os
import sys
from typing import List, Dict, Any

try:
    from rich.console import Console
    from rich.live import Live
    from rich.layout import Layout
    from rich.text import Text
    from rich.align import Align
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

try:
    from blessed import Terminal
    BLESSED_AVAILABLE = True
except ImportError:
    BLESSED_AVAILABLE = False

# Import local modules
from .panels import PanelRenderer
from .tables import TableRenderer
from ..themes.ascii_art import ASCIIArt
from ..themes.animations import Animations


class Display:
    """Main display controller for the application"""
    
    def __init__(self, theme: dict = None):
        self.theme = theme or {
            'primary': 'cyan',
            'secondary': 'yellow',
            'success': 'green',
            'error': 'red',
            'info': 'blue',
            'dim': 'bright_black'
        }
        
        self.panels = PanelRenderer(self.theme)
        self.tables = TableRenderer(self.theme)
        self.animations = Animations()
        
        if RICH_AVAILABLE:
            self.console = Console()
        
        if BLESSED_AVAILABLE:
            self.terminal = Terminal()
    
    def clear(self):
        """Clear the screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def set_theme(self, theme: dict):
        """Update theme"""
        self.theme = theme
        self.panels = PanelRenderer(theme)
        self.tables = TableRenderer(theme)
    
    def show_banner(self, text: str = "DB SEARCH", font: str = 'slant'):
        """Display ASCII art banner"""
        banner = ASCIIArt.generate_banner(text, font)
        
        if RICH_AVAILABLE:
            # Apply gradient colors
            gradient = self.theme.get('gradient', ['cyan', 'bright_cyan', 'white'])
            lines = banner.split('\n')
            
            styled = Text()
            for i, line in enumerate(lines):
                color = gradient[i % len(gradient)]
                styled.append(line + '\n', style=f"bold {color}")
            
            self.console.print(Align.center(styled))
            
            # Subtitle
            self.console.print(Align.center(
                Text("[ Fast Multi-threaded Database Search Engine ]", 
                     style=f"{self.theme['dim']}")
            ))
            self.console.print()
        else:
            print(banner)
            print("[ Fast Multi-threaded Database Search Engine ]")
            print()
    
    def show_header(self, text: str, subtitle: str = None):
        """Display section header"""
        self.panels.header(text, subtitle)
    
    def show_info(self, message: str):
        """Show info message"""
        self.panels.info(message)
    
    def show_success(self, message: str):
        """Show success message"""
        self.panels.success(message)
    
    def show_error(self, message: str):
        """Show error message"""
        self.panels.error(message)
    
    def show_warning(self, message: str):
        """Show warning message"""
        self.panels.warning(message)
    
    def show_results(self, results: List[Dict], stats: dict = None):
        """Display search results"""
        if not results:
            self.panels.warning("No results found", "Search")
            return
        
        if stats:
            self.panels.result_summary(
                count=len(results),
                time_taken=stats.get('search_time', 0),
                files_searched=stats.get('files_searched', 0)
            )
        
        self.tables.render_results(results)
    
    def show_progress(self, iterable, total: int = None, desc: str = "Processing"):
        """Show progress bar for iteration"""
        return self.animations.progress_bar(iterable, total, desc)
    
    def show_spinner(self, text: str = "Loading..."):
        """Start spinner animation"""
        self.animations.spinner_start(text)
    
    def hide_spinner(self, final_text: str = None):
        """Stop spinner animation"""
        self.animations.spinner_stop(final_text)
    
    def typing_effect(self, text: str):
        """Display text with typing effect"""
        self.animations.typing_effect(text)
    
    def show_welcome(self):
        """Show welcome screen"""
        self.clear()
        self.show_banner()
        self.panels.welcome()
    
    def show_goodbye(self):
        """Show goodbye screen"""
        self.panels.goodbye()
    
    def show_stats(self, stats: Dict):
        """Display statistics"""
        self.tables.render_stats(stats)
    
    def print(self, message: str, style: str = None):
        """Print styled message"""
        if RICH_AVAILABLE:
            if style:
                self.console.print(f"[{style}]{message}[/]")
            else:
                self.console.print(message)
        else:
            print(message)
    
    def print_line(self, char: str = '-', width: int = 60):
        """Print a horizontal line"""
        if RICH_AVAILABLE:
            self.console.print(f"[{self.theme['dim']}]{char * width}[/]")
        else:
            print(char * width)
