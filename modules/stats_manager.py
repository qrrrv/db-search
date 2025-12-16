# -*- coding: utf-8 -*-
"""
Advanced Statistics Manager with Charts
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.box import ROUNDED
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


class StatsManager:
    """Advanced statistics collection and display"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.stats_file = os.path.join(config.get('cache_path', 'cache'), 'stats.json')
        self.stats = self._load_stats()
        
        if RICH_AVAILABLE:
            self.console = Console()
    
    def _load_stats(self) -> Dict:
        """Load statistics from file"""
        default_stats = {
            'total_searches': 0,
            'total_results_found': 0,
            'total_search_time': 0,
            'searches_history': [],
            'last_search': None,
            'popular_queries': {},
            'daily_stats': {}
        }
        
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    default_stats.update(loaded)
                    return default_stats
            except:
                pass
        
        return default_stats
    
    def _save_stats(self):
        """Save statistics to file"""
        try:
            os.makedirs(os.path.dirname(self.stats_file), exist_ok=True)
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving statistics: {e}")
    
    def record_search(self, query: str, results_count: int, duration: float):
        """Record search in statistics"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        self.stats['total_searches'] += 1
        self.stats['total_results_found'] += results_count
        self.stats['total_search_time'] += duration
        
        self.stats['last_search'] = {
            'query': query,
            'results': results_count,
            'duration': round(duration, 2),
            'timestamp': datetime.now().isoformat()
        }
        
        # Update history (keep last 100)
        self.stats['searches_history'].append(self.stats['last_search'])
        self.stats['searches_history'] = self.stats['searches_history'][-100:]
        
        # Update popular queries
        query_lower = query.lower()
        if query_lower in self.stats['popular_queries']:
            self.stats['popular_queries'][query_lower] += 1
        else:
            self.stats['popular_queries'][query_lower] = 1
        
        # Update daily stats
        if today not in self.stats['daily_stats']:
            self.stats['daily_stats'][today] = {
                'searches': 0,
                'results': 0,
                'time': 0
            }
        self.stats['daily_stats'][today]['searches'] += 1
        self.stats['daily_stats'][today]['results'] += results_count
        self.stats['daily_stats'][today]['time'] += duration
        
        self._save_stats()
    
    def show_statistics(self):
        """Display comprehensive statistics"""
        db_path = self.config.get('database_path', 'bd')
        
        # Collect database info
        total_files = 0
        total_size = 0
        file_types = {'txt': 0, 'csv': 0}
        
        if os.path.exists(db_path):
            for root, dirs, files in os.walk(db_path):
                for f in files:
                    if f.endswith('.txt'):
                        total_files += 1
                        file_types['txt'] += 1
                        try:
                            total_size += os.path.getsize(os.path.join(root, f))
                        except:
                            pass
                    elif f.endswith('.csv'):
                        total_files += 1
                        file_types['csv'] += 1
                        try:
                            total_size += os.path.getsize(os.path.join(root, f))
                        except:
                            pass
        
        size_gb = total_size / (1024 ** 3)
        size_mb = total_size / (1024 ** 2)
        
        # Calculate averages
        avg_results = 0
        avg_time = 0
        if self.stats['total_searches'] > 0:
            avg_results = self.stats['total_results_found'] / self.stats['total_searches']
            avg_time = self.stats['total_search_time'] / self.stats['total_searches']
        
        if RICH_AVAILABLE:
            # Database panel
            db_info = f"""[cyan]Total Files:[/] [yellow]{total_files}[/]
[cyan]TXT Files:[/] [yellow]{file_types['txt']}[/]
[cyan]CSV Files:[/] [yellow]{file_types['csv']}[/]
[cyan]Total Size:[/] [yellow]{size_gb:.2f} GB ({size_mb:.0f} MB)[/]
[cyan]Path:[/] [yellow]{db_path}[/]"""
            
            self.console.print(Panel(db_info, title="DATABASE INFO", border_style="blue"))
            
            # Search stats panel
            search_info = f"""[cyan]Total Searches:[/] [green]{self.stats['total_searches']}[/]
[cyan]Total Results Found:[/] [green]{self.stats['total_results_found']:,}[/]
[cyan]Total Search Time:[/] [green]{self.stats['total_search_time']:.1f} sec[/]
[cyan]Average Results:[/] [green]{avg_results:.1f}[/]
[cyan]Average Time:[/] [green]{avg_time:.2f} sec[/]"""
            
            self.console.print(Panel(search_info, title="SEARCH STATISTICS", border_style="green"))
            
            # Last search
            if self.stats['last_search']:
                last = self.stats['last_search']
                last_info = f"""[cyan]Query:[/] [yellow]{last['query']}[/]
[cyan]Results:[/] [yellow]{last['results']}[/]
[cyan]Time:[/] [yellow]{last['duration']} sec[/]
[cyan]Date:[/] [yellow]{last['timestamp'][:19]}[/]"""
                
                self.console.print(Panel(last_info, title="LAST SEARCH", border_style="yellow"))
            
            # Popular queries
            if self.stats['popular_queries']:
                sorted_queries = sorted(
                    self.stats['popular_queries'].items(), 
                    key=lambda x: x[1], 
                    reverse=True
                )[:10]
                
                table = Table(title="TOP 10 POPULAR QUERIES", box=ROUNDED, border_style="magenta")
                table.add_column("#", style="dim", width=4)
                table.add_column("Query", style="cyan", width=30)
                table.add_column("Count", style="green", width=10)
                
                for i, (query, count) in enumerate(sorted_queries, 1):
                    table.add_row(str(i), query[:30], str(count))
                
                self.console.print(table)
            
            # Daily chart (simple text chart)
            if self.stats['daily_stats']:
                dates = sorted(self.stats['daily_stats'].keys())[-7:]  # Last 7 days
                
                self.console.print("\n[bold cyan]LAST 7 DAYS ACTIVITY:[/]")
                max_searches = max(self.stats['daily_stats'][d]['searches'] for d in dates) or 1
                
                for date in dates:
                    day_stats = self.stats['daily_stats'][date]
                    bar_len = int((day_stats['searches'] / max_searches) * 30)
                    bar = "[green]" + "█" * bar_len + "[/]" + "░" * (30 - bar_len)
                    self.console.print(f"  {date}: {bar} {day_stats['searches']} searches")
        
        else:
            # Simple text output
            print("\n" + "=" * 60)
            print("                    STATISTICS")
            print("=" * 60)
            print(f"""
  DATABASE:
     Files:      {total_files} (TXT: {file_types['txt']}, CSV: {file_types['csv']})
     Size:       {size_gb:.2f} GB ({size_mb:.0f} MB)
     Path:       {db_path}

  SEARCHES:
     Total:      {self.stats['total_searches']}
     Results:    {self.stats['total_results_found']:,}
     Avg time:   {avg_time:.2f} sec""")
            
            if self.stats['last_search']:
                last = self.stats['last_search']
                print(f"""
  LAST SEARCH:
     Query:      {last['query']}
     Results:    {last['results']}
     Time:       {last['duration']} sec""")
            
            print("\n" + "=" * 60)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics dictionary"""
        return self.stats.copy()
    
    def clear_stats(self):
        """Clear all statistics"""
        self.stats = {
            'total_searches': 0,
            'total_results_found': 0,
            'total_search_time': 0,
            'searches_history': [],
            'last_search': None,
            'popular_queries': {},
            'daily_stats': {}
        }
        self._save_stats()