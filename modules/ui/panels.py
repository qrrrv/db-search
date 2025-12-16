# -*- coding: utf-8 -*-
"""
Panel Renderer - Beautiful bordered panels
"""

from typing import Optional

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.box import ROUNDED, DOUBLE, HEAVY, SIMPLE
    from rich.align import Align
    from rich.text import Text
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


class PanelRenderer:
    """Renders beautiful panels and boxes"""
    
    def __init__(self, theme: dict = None):
        self.theme = theme or {
            'primary': 'cyan',
            'secondary': 'yellow',
            'success': 'green',
            'error': 'red',
            'info': 'blue'
        }
        
        if RICH_AVAILABLE:
            self.console = Console()
    
    def info(self, message: str, title: str = "Info"):
        """Display info panel"""
        self._render_panel(message, title, 'info', 'blue')
    
    def success(self, message: str, title: str = "Success"):
        """Display success panel"""
        self._render_panel(message, title, 'success', 'green')
    
    def error(self, message: str, title: str = "Error"):
        """Display error panel"""
        self._render_panel(message, title, 'error', 'red')
    
    def warning(self, message: str, title: str = "Warning"):
        """Display warning panel"""
        self._render_panel(message, title, 'secondary', 'yellow')
    
    def header(self, text: str, subtitle: str = None):
        """Display header panel"""
        if RICH_AVAILABLE:
            styled_text = Text(text, style=f"bold {self.theme['primary']}")
            
            content = Align.center(styled_text)
            
            self.console.print(Panel(
                content,
                border_style=self.theme['primary'],
                box=DOUBLE,
                subtitle=subtitle
            ))
        else:
            print("\n" + "=" * 60)
            print(f"  {text}")
            if subtitle:
                print(f"  {subtitle}")
            print("=" * 60)
    
    def box(self, content: str, title: str = None, border_style: str = 'primary'):
        """Display content in a box"""
        if RICH_AVAILABLE:
            self.console.print(Panel(
                content,
                title=title,
                border_style=self.theme.get(border_style, 'cyan'),
                box=ROUNDED
            ))
        else:
            width = max(len(line) for line in content.split('\n')) + 4
            print("+" + "-" * (width - 2) + "+")
            if title:
                print(f"| {title.center(width - 4)} |")
                print("+" + "-" * (width - 2) + "+")
            for line in content.split('\n'):
                print(f"| {line.ljust(width - 4)} |")
            print("+" + "-" * (width - 2) + "+")
    
    def _render_panel(self, message: str, title: str, style_key: str, fallback_color: str):
        """Internal method to render a panel"""
        if RICH_AVAILABLE:
            color = self.theme.get(style_key, fallback_color)
            self.console.print(Panel(
                f"[{color}]{message}[/]",
                title=f"[bold]{title}[/]",
                border_style=color,
                box=ROUNDED
            ))
        else:
            print(f"\n[{title}] {message}\n")
    
    def result_summary(self, count: int, time_taken: float, files_searched: int):
        """Display search result summary"""
        if RICH_AVAILABLE:
            content = (
                f"[{self.theme['success']}]Found: {count} results[/]\n"
                f"[{self.theme['info']}]Time: {time_taken:.2f} seconds[/]\n"
                f"[{self.theme['primary']}]Files searched: {files_searched}[/]"
            )
            self.console.print(Panel(
                content,
                title="[bold]Search Complete[/]",
                border_style=self.theme['success'],
                box=ROUNDED
            ))
        else:
            print(f"\n[Search Complete]")
            print(f"  Found: {count} results")
            print(f"  Time: {time_taken:.2f} seconds")
            print(f"  Files: {files_searched}")
    
    def welcome(self, version: str = "2.0"):
        """Display welcome panel"""
        if RICH_AVAILABLE:
            content = (
                f"[bold {self.theme['primary']}]DATABASE SEARCH TOOL[/]\n"
                f"[{self.theme['secondary']}]Version {version} PRO[/]\n\n"
                f"[{self.theme['info']}]Features:[/]\n"
                f"  [green]*[/] Multi-threaded search\n"
                f"  [green]*[/] Support for 20-70GB databases\n"
                f"  [green]*[/] Beautiful themed interface\n"
                f"  [green]*[/] Export to multiple formats\n"
            )
            self.console.print(Panel(
                Align.center(content),
                border_style=self.theme['primary'],
                box=DOUBLE
            ))
        else:
            print("\n" + "=" * 50)
            print("  DATABASE SEARCH TOOL v2.0 PRO")
            print("=" * 50)
            print("  * Multi-threaded search")
            print("  * Support for large databases")
            print("  * Export to multiple formats")
            print("=" * 50)
    
    def goodbye(self):
        """Display goodbye panel"""
        if RICH_AVAILABLE:
            self.console.print(Panel(
                Align.center(Text(
                    "Thanks for using DB Search Tool!\nGoodbye!",
                    style=f"bold {self.theme['primary']}"
                )),
                border_style=self.theme['primary'],
                box=DOUBLE
            ))
        else:
            print("\n" + "=" * 40)
            print("  Thanks for using DB Search Tool!")
            print("  Goodbye!")
            print("=" * 40 + "\n")
