# -*- coding: utf-8 -*-
"""
Table Renderer - Beautiful table output
"""

from typing import List, Dict, Any, Optional

try:
    from rich.console import Console
    from rich.table import Table
    from rich.box import ROUNDED, DOUBLE, SIMPLE, HEAVY, MINIMAL, ASCII
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

try:
    from tabulate import tabulate
    TABULATE_AVAILABLE = True
except ImportError:
    TABULATE_AVAILABLE = False


class TableRenderer:
    """Renders beautiful tables in console"""
    
    BOX_STYLES = {
        'rounded': ROUNDED if RICH_AVAILABLE else None,
        'double': DOUBLE if RICH_AVAILABLE else None,
        'simple': SIMPLE if RICH_AVAILABLE else None,
        'heavy': HEAVY if RICH_AVAILABLE else None,
        'minimal': MINIMAL if RICH_AVAILABLE else None,
        'ascii': ASCII if RICH_AVAILABLE else None,
    }
    
    TABULATE_FORMATS = [
        'fancy_grid', 'grid', 'simple', 'pipe', 'orgtbl',
        'rst', 'mediawiki', 'html', 'latex', 'plain'
    ]
    
    def __init__(self, theme: dict = None):
        self.theme = theme or {
            'primary': 'cyan',
            'secondary': 'yellow',
            'header': 'bold magenta',
            'row_odd': '',
            'row_even': 'dim'
        }
        
        if RICH_AVAILABLE:
            self.console = Console()
    
    def render(self, data: List[Dict], title: str = None, 
               columns: List[str] = None, box_style: str = 'rounded',
               max_width: int = None) -> str:
        """Render data as a table"""
        if not data:
            return "No data to display"
        
        if columns is None:
            columns = list(data[0].keys())
        
        if RICH_AVAILABLE:
            return self._render_rich(data, title, columns, box_style, max_width)
        elif TABULATE_AVAILABLE:
            return self._render_tabulate(data, title, columns)
        else:
            return self._render_simple(data, title, columns)
    
    def _render_rich(self, data: List[Dict], title: str, 
                     columns: List[str], box_style: str, max_width: int) -> str:
        """Render using Rich library"""
        box = self.BOX_STYLES.get(box_style, ROUNDED)
        
        table = Table(
            title=title,
            title_style=f"bold {self.theme['secondary']}",
            box=box,
            border_style=self.theme['primary'],
            header_style=self.theme['header'],
            row_styles=[self.theme['row_odd'], self.theme['row_even']],
            expand=False
        )
        
        # Add columns
        for col in columns:
            col_width = max_width // len(columns) if max_width else None
            table.add_column(col.replace('_', ' ').title(), max_width=col_width)
        
        # Add rows
        for row in data:
            values = [str(row.get(col, ''))[:50] for col in columns]
            table.add_row(*values)
        
        self.console.print(table)
        return ""
    
    def _render_tabulate(self, data: List[Dict], title: str, columns: List[str]) -> str:
        """Render using tabulate library"""
        if title:
            print(f"\n  {title}")
            print("  " + "=" * 50)
        
        rows = [[row.get(col, '') for col in columns] for row in data]
        headers = [col.replace('_', ' ').title() for col in columns]
        
        output = tabulate(rows, headers=headers, tablefmt='fancy_grid')
        print(output)
        return output
    
    def _render_simple(self, data: List[Dict], title: str, columns: List[str]) -> str:
        """Render simple ASCII table"""
        if title:
            print(f"\n  {title}")
            print("  " + "=" * 60)
        
        # Calculate column widths
        widths = {}
        for col in columns:
            max_len = len(col)
            for row in data:
                val_len = len(str(row.get(col, '')))
                if val_len > max_len:
                    max_len = min(val_len, 20)  # Max 20 chars
            widths[col] = max_len
        
        # Header
        header = " | ".join(col.ljust(widths[col])[:widths[col]] for col in columns)
        print(f"  {header}")
        print("  " + "-" * len(header))
        
        # Rows
        for row in data:
            line = " | ".join(
                str(row.get(col, '')).ljust(widths[col])[:widths[col]] 
                for col in columns
            )
            print(f"  {line}")
        
        return ""
    
    def render_results(self, results: List[Dict], limit: int = 50):
        """Render search results in a nice table"""
        if not results:
            if RICH_AVAILABLE:
                self.console.print(f"[{self.theme['secondary']}]No results found[/]")
            else:
                print("No results found")
            return
        
        display_data = []
        for i, r in enumerate(results[:limit], 1):
            parsed = r.get('parsed', {})
            display_data.append({
                '#': i,
                'file': r.get('file', 'N/A')[:20],
                'line': r.get('line_number', 'N/A'),
                'data': str(parsed or r.get('raw_data', ''))[:40]
            })
        
        self.render(
            display_data, 
            title=f"Search Results ({len(results)} found)",
            columns=['#', 'file', 'line', 'data'],
            box_style='rounded'
        )
        
        if len(results) > limit:
            if RICH_AVAILABLE:
                self.console.print(
                    f"\n[{self.theme['primary']}]... and {len(results) - limit} more results. "
                    f"Export to see all.[/]"
                )
            else:
                print(f"\n... and {len(results) - limit} more results.")
    
    def render_stats(self, stats: Dict):
        """Render statistics table"""
        data = [{'metric': k, 'value': v} for k, v in stats.items()]
        self.render(data, title="Statistics", columns=['metric', 'value'])
