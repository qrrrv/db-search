# -*- coding: utf-8 -*-
"""
Menu System - Beautiful console menus
"""

import os
from typing import List, Dict, Callable, Optional, Any

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.box import ROUNDED, DOUBLE, HEAVY
    from rich.align import Align
    from rich.text import Text
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

try:
    from blessed import Terminal
    BLESSED_AVAILABLE = True
except ImportError:
    BLESSED_AVAILABLE = False


class MenuItem:
    """Single menu item"""
    
    def __init__(self, key: str, label: str, action: Callable = None, 
                 icon: str = "", description: str = "", enabled: bool = True):
        self.key = key
        self.label = label
        self.action = action
        self.icon = icon
        self.description = description
        self.enabled = enabled


class Menu:
    """Beautiful console menu system"""
    
    def __init__(self, title: str = "Menu", theme: dict = None):
        self.title = title
        self.items: List[MenuItem] = []
        self.theme = theme or {
            'primary': 'cyan',
            'secondary': 'yellow',
            'success': 'green',
            'error': 'red',
            'dim': 'bright_black'
        }
        
        if RICH_AVAILABLE:
            self.console = Console()
        else:
            self.console = None
    
    def add_item(self, key: str, label: str, action: Callable = None, 
                 icon: str = "", description: str = "", enabled: bool = True):
        """Add item to menu"""
        self.items.append(MenuItem(key, label, action, icon, description, enabled))
    
    def add_separator(self):
        """Add separator line"""
        self.items.append(MenuItem("---", "---", None))
    
    def clear(self):
        """Clear all menu items"""
        self.items = []
    
    def display(self) -> str:
        """Display menu and get user choice"""
        if RICH_AVAILABLE:
            return self._display_rich()
        elif BLESSED_AVAILABLE:
            return self._display_blessed()
        else:
            return self._display_simple()
    
    def _display_rich(self) -> str:
        """Display menu using Rich library"""
        table = Table(
            title=self.title,
            title_style=f"bold {self.theme['secondary']}",
            box=ROUNDED,
            border_style=self.theme['primary'],
            show_header=False,
            padding=(0, 2),
            expand=False
        )
        
        table.add_column("Key", style=self.theme['success'], width=6, justify="center")
        table.add_column("Action", style="white", width=35)
        table.add_column("Description", style=self.theme['dim'], width=25)
        
        for item in self.items:
            if item.key == "---":
                table.add_row("", "-" * 30, "")
            elif item.key in ['0', 'q', 'Q']:
                table.add_row(
                    f"[red]{item.key}[/]",
                    f"[red]{item.icon} {item.label}[/]",
                    f"[{self.theme['dim']}]{item.description}[/]"
                )
            else:
                style = "" if item.enabled else "dim strike"
                table.add_row(
                    f"[{self.theme['success']}]{item.key}[/]",
                    f"{item.icon} {item.label}",
                    item.description
                )
        
        self.console.print()
        self.console.print(Align.center(table))
        self.console.print()
        
        self.console.print(f"[{self.theme['primary']}]Enter choice: [/]", end="")
        return input().strip()
    
    def _display_blessed(self) -> str:
        """Display menu using Blessed library"""
        term = Terminal()
        
        print(term.clear)
        print(term.bold_cyan(f"\n  {self.title}"))
        print("  " + "=" * 40)
        
        for item in self.items:
            if item.key == "---":
                print("  " + "-" * 40)
            elif item.key in ['0', 'q']:
                print(term.red(f"  [{item.key}] {item.icon} {item.label}"))
            else:
                print(term.green(f"  [{item.key}]") + f" {item.icon} {item.label}")
        
        print()
        return input(term.cyan("  > ")).strip()
    
    def _display_simple(self) -> str:
        """Display simple ASCII menu"""
        print(f"\n  {self.title}")
        print("  " + "=" * 40)
        
        for item in self.items:
            if item.key == "---":
                print("  " + "-" * 40)
            else:
                status = "" if item.enabled else " (disabled)"
                print(f"  [{item.key}] {item.icon} {item.label}{status}")
        
        print()
        return input("  > ").strip()
    
    def run(self) -> Optional[Any]:
        """Run menu loop until exit"""
        while True:
            choice = self.display()
            
            for item in self.items:
                if item.key == choice and item.enabled:
                    if item.action:
                        result = item.action()
                        if result == 'exit':
                            return None
                        if result:
                            return result
                    elif choice in ['0', 'q', 'Q']:
                        return None
                    break
            else:
                if RICH_AVAILABLE:
                    self.console.print(f"[{self.theme['error']}]Invalid choice. Try again.[/]")
                else:
                    print("Invalid choice. Try again.")


class SubMenu(Menu):
    """Submenu with back option"""
    
    def __init__(self, title: str, parent_title: str = "Main Menu", theme: dict = None):
        super().__init__(title, theme)
        self.parent_title = parent_title
    
    def display(self) -> str:
        """Display submenu with back option"""
        # Automatically add back option if not present
        has_back = any(item.key in ['0', 'b', 'B'] for item in self.items)
        if not has_back:
            self.add_item('0', f'Back to {self.parent_title}', icon='<-')
        
        return super().display()