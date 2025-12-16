# -*- coding: utf-8 -*-
"""
UI Manager with Animated Themes - FIXED VERSION
"""

import os
import sys
import time
import threading
from typing import List, Dict, Any

# Import theme loader
try:
    from modules.themes.theme_loader import ThemeLoader
    THEMES_AVAILABLE = True
except ImportError:
    THEMES_AVAILABLE = False

# Rich library
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.box import ROUNDED, DOUBLE, HEAVY
    from rich.align import Align
    from rich.text import Text
    from rich.live import Live
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

# Colorama
try:
    from colorama import init, Fore, Style as CStyle
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False

# Pyfiglet for ASCII art
try:
    from pyfiglet import Figlet
    PYFIGLET_AVAILABLE = True
except ImportError:
    PYFIGLET_AVAILABLE = False

# ART library
try:
    from art import text2art
    ART_AVAILABLE = True
except ImportError:
    ART_AVAILABLE = False

# Halo spinners
try:
    from halo import Halo
    HALO_AVAILABLE = True
except ImportError:
    HALO_AVAILABLE = False

# Alive progress
try:
    from alive_progress import alive_bar
    ALIVE_AVAILABLE = True
except ImportError:
    ALIVE_AVAILABLE = False


class UIManager:
    """Beautiful UI Manager with Animated Themes"""
    
    def __init__(self, config):
        self.config = config
        
        # Initialize theme loader
        if THEMES_AVAILABLE:
            self.theme_loader = ThemeLoader()
            saved_theme = config.get('theme', 'default')
            self.theme_loader.set_theme(saved_theme)
        else:
            self.theme_loader = None
        
        if RICH_AVAILABLE:
            self.console = Console()
        else:
            self.console = None
        
        self._animation_running = False
    
    def get_theme(self):
        """Get current theme"""
        if self.theme_loader:
            return self.theme_loader.get_current_theme()
        return None
    
    def set_theme(self, theme_name):
        """Set theme and save to config"""
        if self.theme_loader:
            self.theme_loader.set_theme(theme_name)
            self.config.set('theme', theme_name)
    
    def clear_screen(self):
        """Clear console"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_banner(self):
        """Show animated ASCII art banner"""
        theme = self.get_theme()
        
        if RICH_AVAILABLE and theme:
            self._show_animated_banner(theme)
        else:
            self._show_simple_banner()
    
    def _show_animated_banner(self, theme):
        """Show banner with theme colors"""
        # Get custom banner text and font from theme
        banner_text_str = theme.config.get('banner_text', 'DB SEARCH')
        banner_font = theme.config.get('banner_font', 'slant')
        
        # Generate ASCII art
        banner_text = self._generate_ascii_art(banner_text_str, banner_font)
        
        # Apply gradient colors
        lines = banner_text.split('\n')
        styled = Text()
        
        for i, line in enumerate(lines):
            color = theme.gradient[i % len(theme.gradient)]
            styled.append(line + '\n', style=f"bold {color}")
        
        # Create panel
        panel = Panel(
            Align.center(styled),
            border_style=theme.primary,
            box=DOUBLE,
            title=f"[bold {theme.secondary}]v2.0 PRO[/]",
            subtitle=f"[{theme.dim}]Theme: {theme.display_name}[/]"
        )
        
        self.console.print(panel)
        
        # Subtitle
        subtitle = Text()
        features = "Fast Search | Multi-threading | Large DB Support | 15 Themes"
        for i, char in enumerate(features):
            color = theme.gradient[i % len(theme.gradient)]
            subtitle.append(char, style=color)
        
        self.console.print(Align.center(subtitle))
        self.console.print()
    
    def _generate_ascii_art(self, text, font='slant'):
        """Generate ASCII art"""
        if PYFIGLET_AVAILABLE:
            try:
                fig = Figlet(font=font)
                return fig.renderText(text)
            except:
                try:
                    # Fallback to slant if custom font fails
                    fig = Figlet(font='slant')
                    return fig.renderText(text)
                except:
                    pass
        
        if ART_AVAILABLE:
            try:
                return text2art(text, font=font)
            except:
                pass
        
        # Ultimate fallback
        return f"""
    ____  ____     _____ _____    _    ____   ____ _   _ 
   |  _ \\| __ )   / ___|| ____|  / \\  |  _ \\ / ___| | | |
   | | | |  _ \\   \___ \|  _|   / _ \ | |_) | |   | |_| |
   | |_| | |_) |   ___) | |___ / ___ \|  _ <| |___|  _  |
   |____/|____/   |____/|_____/_/   \_\_| \_\\____|_| |_|
"""
    
    def _show_simple_banner(self):
        """Simple banner without Rich"""
        print("""
    ____  ____     _____ _____    _    ____   ____ _   _ 
   |  _ \\| __ )   / ___|| ____|  / \\  |  _ \\ / ___| | | |
   | | | |  _ \\   \___ \|  _|   / _ \ | |_) | |   | |_| |
   | |_| | |_) |   ___) | |___ / ___ \|  _ <| |___|  _  |
   |____/|____/   |____/|_____/_/   \_\_| \_\\____|_| |_|
                                                    
            === DATABASE SEARCH TOOL v2.0 ===
""")
    
    def show_menu(self):
        """Show main menu with current theme indicator"""
        theme = self.get_theme()
        
        if RICH_AVAILABLE and theme:
            self._show_rich_menu(theme)
        else:
            self._show_simple_menu()
    
    def _show_rich_menu(self, theme):
        """Show Rich styled menu"""
        menu_items = [
            ("1", "Search in databases", "Find data by any criteria"),
            ("2", "Index databases", "Pre-index for faster search"),
            ("3", "Statistics", "View search stats"),
            ("4", "Settings", "Configure the tool"),
            ("5", "Clear cache", "Free up cache space"),
            ("6", "Database info", "View database details"),
            ("7", f"Change theme [{theme.name}]", "Choose from 15 themes"),
            ("0", "Exit", "Close the program"),
        ]
        
        table = Table(
            title=f"MAIN MENU",
            title_style=f"bold {theme.secondary}",
            box=ROUNDED,
            border_style=theme.primary,
            show_header=False,
            padding=(0, 2),
            caption=f"[{theme.dim}]Current theme: {theme.display_name} [*][/]"
        )
        
        table.add_column("Key", style=theme.success, width=5)
        table.add_column("Action", style="white", width=30, no_wrap=True)
        table.add_column("Description", style=theme.dim, width=30, no_wrap=True)
        
        for key, action, desc in menu_items:
            if key == "0":
                table.add_row(f"[{theme.error}]{key}[/]", 
                             f"[{theme.error}]{action}[/]", 
                             f"[{theme.error}]{desc}[/]")
            elif key == "7":
                # Highlight theme option
                table.add_row(f"[{theme.secondary}]{key}[/]", 
                             f"[{theme.secondary}]{action}[/]", 
                             f"[{theme.info}]{desc}[/]")
            else:
                table.add_row(f"[{theme.success}]{key}[/]", action, desc)
        
        self.console.print()
        self.console.print(Align.center(table))
        self.console.print()
    
    def _show_simple_menu(self):
        """Simple ASCII menu"""
        print("""
+==================================================+
|                  MAIN MENU                       |
+==================================================+
|                                                  |
|  [1] Search in databases                         |
|  [2] Index databases                             |
|  [3] Statistics                                  |
|  [4] Settings                                    |
|  [5] Clear cache                                 |
|  [6] Database info                               |
|  [7] Change theme                                |
|  [0] Exit                                        |
|                                                  |
+==================================================+
""")
    
    def get_user_choice(self):
        """Get menu choice"""
        theme = self.get_theme()
        if RICH_AVAILABLE and theme:
            self.console.print(f"[{theme.primary}]Enter choice: [/]", end="")
        else:
            print("Enter choice: ", end="")
        return input().strip()
    
    def get_search_query(self):
        """Get search query with examples"""
        theme = self.get_theme()
        
        if RICH_AVAILABLE and theme:
            panel = Panel(
                f"[{theme.secondary}]Enter your search query:[/]\n\n"
                f"[{theme.dim}]Examples:\n"
                f"  - Telegram ID: 123456789\n"
                f"  - Phone: +79001234567\n"
                f"  - Name: John Smith\n"
                f"  - Email: example@mail.com\n"
                f"  - Username: @username[/]",
                border_style=theme.info,
                title="SEARCH"
            )
            self.console.print(panel)
            self.console.print(f"[{theme.success}]Search: [/]", end="")
        else:
            print("\nEnter search query:")
            print("Search: ", end="")
        
        return input()
    
    def show_search_header(self):
        """Show search header"""
        theme = self.get_theme()
        if RICH_AVAILABLE and theme:
            header = Panel(
                Align.center(Text("SEARCH IN DATABASES", style=f"bold {theme.primary}")),
                border_style=theme.primary,
                box=HEAVY
            )
            self.console.print(header)
        else:
            print("\n" + "=" * 50)
            print("       SEARCH IN DATABASES")
            print("=" * 50)
    
    def show_progress_start(self):
        """Show search progress"""
        theme = self.get_theme()
        
        if HALO_AVAILABLE and theme:
            color = theme.primary.replace('bright_', '')
            self._spinner = Halo(text='Searching...', spinner='dots', color=color)
            self._spinner.start()
        elif RICH_AVAILABLE:
            self.console.print(f"\n[bold]Searching...[/]")
        else:
            print("\nSearching...")
    
    def show_progress_stop(self, success=True):
        """Stop progress"""
        if HALO_AVAILABLE and hasattr(self, '_spinner'):
            if success:
                self._spinner.succeed('Search complete!')
            else:
                self._spinner.fail('Search failed')
    
    def show_results(self, results, stats=None):
        """Show search results"""
        theme = self.get_theme()
        
        if not results:
            if RICH_AVAILABLE and theme:
                self.console.print(Panel(
                    Align.center(Text("Nothing found", style=f"bold {theme.error}")),
                    border_style=theme.error
                ))
            else:
                print("\nNothing found\n")
            return
        
        if RICH_AVAILABLE and theme:
            self._show_rich_results(results, theme)
        else:
            self._show_simple_results(results)
    
    def _show_rich_results(self, results, theme):
        """Show results with Rich"""
        # Animated summary with gradient
        summary_text = Text()
        msg = f"Found: {len(results)} results"
        for i, char in enumerate(msg):
            color = theme.gradient[i % len(theme.gradient)]
            summary_text.append(char, style=f"bold {color}")
        
        self.console.print(Panel(
            Align.center(summary_text),
            border_style=theme.success
        ))
        
        # Table with full data display
        table = Table(
            title="Search Results",
            box=ROUNDED,
            border_style=theme.primary,
            header_style=f"bold {theme.secondary}",
            show_lines=True,
            expand=True  # Expand table to full width
        )
        
        table.add_column("#", style="dim", width=4)
        table.add_column("File", style=theme.info, width=25)
        table.add_column("Line", style=theme.secondary, width=8)
        table.add_column("Full Data", style=theme.success, no_wrap=False)  # No wrapping - show in one line
        
        for i, result in enumerate(results[:50], 1):
            # Show full raw data without truncation
            full_data = result.get('raw_data', '')
            
            # Clean data - remove "Нет" and extra semicolons
            full_data = full_data.replace(';Нет;', ';;').replace(';Нет', ';').replace('Нет;', ';')
            full_data = full_data.replace(';;', ';')  # Remove double semicolons
            
            table.add_row(
                str(i),
                result.get('file', 'N/A')[:25],
                str(result.get('line_number', 'N/A')),
                full_data  # Full data - clean and no truncation!
            )
        
        self.console.print(table)
        
        if len(results) > 50:
            self.console.print(f"\n[{theme.dim}]... and {len(results) - 50} more results. Export to see all.[/]")
    
    def _show_simple_results(self, results):
        """Simple results display"""
        print(f"\nFound: {len(results)} results\n")
        print("-" * 70)
        
        for i, result in enumerate(results[:50], 1):
            # Clean data - remove "Нет"
            full_data = result.get('raw_data', '')
            full_data = full_data.replace(';Нет;', ';;').replace(';Нет', ';').replace('Нет;', ';')
            full_data = full_data.replace(';;', ';')
            
            print(f"[{i}] {result.get('file', 'N/A')} (line {result.get('line_number', 'N/A')})")
            print(f"    {full_data}")  # Full data - clean
            print("-" * 70)
    
    def show_theme_selector(self):
        """Show theme selector with animations"""
        if self.theme_loader:
            return self.theme_loader.show_theme_selector()
        return 'default'
    
    def show_indexing_header(self):
        """Show indexing header"""
        theme = self.get_theme()
        if RICH_AVAILABLE and theme:
            self.console.print(Panel(
                Align.center(Text("INDEXING DATABASES", style=f"bold {theme.primary}")),
                border_style=theme.primary
            ))
        else:
            print("\n=== INDEXING DATABASES ===\n")
    
    def show_indexing_complete(self, stats):
        """Show indexing complete"""
        theme = self.get_theme()
        size_mb = stats.get('total_size', 0) / (1024 * 1024)
        
        if RICH_AVAILABLE and theme:
            content = f"""[bold {theme.success}]Indexing Complete![/]

[{theme.info}]Files indexed:[/] [{theme.secondary}]{stats.get('files', 0)}[/]
[{theme.info}]Records found:[/] [{theme.secondary}]{stats.get('records', 0):,}[/]
[{theme.info}]Total size:[/] [{theme.secondary}]{size_mb:.2f} MB[/]
[{theme.info}]Time:[/] [{theme.secondary}]{stats.get('time', 0):.2f} sec[/]"""
            
            self.console.print(Panel(content, border_style=theme.success, title="COMPLETE"))
        else:
            print(f"\nIndexing complete!")
            print(f"  Files: {stats.get('files', 0)}")
            print(f"  Records: {stats.get('records', 0):,}")
    
    def ask_export(self):
        """Ask about export"""
        theme = self.get_theme()
        if RICH_AVAILABLE and theme:
            self.console.print(f"\n[{theme.secondary}]Export results to file? (y/n)[/]")
        else:
            print("\nExport results? (y/n)")
        return input("> ").strip().lower() in ['y', 'yes']
    
    def show_export_success(self, filepath=None):
        """Show export success"""
        theme = self.get_theme()
        msg = f"Exported to: {filepath}" if filepath else "Results exported"
        if RICH_AVAILABLE and theme:
            self.console.print(Panel(f"[bold {theme.success}]{msg}[/]", border_style=theme.success))
        else:
            print(f"\n{msg}")
    
    def show_cache_cleared(self):
        """Show cache cleared"""
        theme = self.get_theme()
        if RICH_AVAILABLE and theme:
            self.console.print(f"[bold {theme.success}]Cache cleared![/]")
        else:
            print("Cache cleared")
    
    def show_invalid_choice(self):
        """Show invalid choice"""
        theme = self.get_theme()
        if RICH_AVAILABLE and theme:
            self.console.print(f"[bold {theme.error}]Invalid choice.[/]")
        else:
            print("Invalid choice")
    
    def show_goodbye(self):
        """Show goodbye message"""
        theme = self.get_theme()
        
        if RICH_AVAILABLE and theme:
            text = Text()
            goodbye = "Thanks for using DB Search Tool! Goodbye!"
            
            for i, char in enumerate(goodbye):
                color = theme.gradient[i % len(theme.gradient)]
                text.append(char, style=f"bold {color}")
            
            self.console.print(Panel(
                Align.center(text),
                border_style=theme.primary,
                box=DOUBLE
            ))
        else:
            print("\nGoodbye!\n")
    
    def wait_for_key(self):
        """Wait for key press"""
        theme = self.get_theme()
        if RICH_AVAILABLE and theme:
            self.console.print(f"\n[{theme.dim}]Press Enter to continue...[/]")
        else:
            print("\nPress Enter to continue...")
        input()
    
    def show_error(self, message):
        """Show error"""
        theme = self.get_theme()
        if RICH_AVAILABLE and theme:
            self.console.print(Panel(
                f"[bold {theme.error}]ERROR: {message}[/]",
                border_style=theme.error
            ))
        else:
            print(f"[ERROR] {message}")
    
    def show_info(self, message):
        """Show info"""
        theme = self.get_theme()
        if RICH_AVAILABLE and theme:
            self.console.print(f"[{theme.info}]{message}[/]")
        else:
            print(message)