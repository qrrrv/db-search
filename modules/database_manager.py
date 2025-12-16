# -*- coding: utf-8 -*-
"""
Advanced Database Manager with Analysis
"""

import os
from typing import Dict, List, Any
from datetime import datetime

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.tree import Tree
    from rich.box import ROUNDED
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


class DatabaseManager:
    """Advanced database management with visualization"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.db_path = config.get('database_path', 'bd')
        
        os.makedirs(self.db_path, exist_ok=True)
        
        if RICH_AVAILABLE:
            self.console = Console()
    
    def get_database_list(self) -> List[Dict[str, Any]]:
        """Get list of all databases with metadata"""
        databases = []
        extensions = self.config.get('file_extensions', ['.txt', '.csv'])
        
        for root, dirs, files in os.walk(self.db_path):
            for filename in files:
                if any(filename.lower().endswith(ext) for ext in extensions):
                    filepath = os.path.join(root, filename)
                    
                    try:
                        stat = os.stat(filepath)
                        
                        # Count lines (sample for large files)
                        lines = self._count_lines_fast(filepath)
                        
                        databases.append({
                            'name': filename,
                            'path': filepath,
                            'relative_path': os.path.relpath(filepath, self.db_path),
                            'folder': os.path.relpath(root, self.db_path) or '.',
                            'size': stat.st_size,
                            'size_mb': stat.st_size / (1024 * 1024),
                            'size_gb': stat.st_size / (1024 ** 3),
                            'modified': datetime.fromtimestamp(stat.st_mtime),
                            'type': os.path.splitext(filename)[1].lower(),
                            'lines': lines
                        })
                    except Exception as e:
                        self.logger.error(f"Error getting info for {filepath}: {e}")
        
        return databases
    
    def _count_lines_fast(self, filepath: str, sample_size: int = 1024*1024) -> int:
        """Fast line count estimation"""
        try:
            file_size = os.path.getsize(filepath)
            
            if file_size < sample_size:
                # Small file - count all lines
                with open(filepath, 'rb') as f:
                    return sum(1 for _ in f)
            else:
                # Large file - estimate
                with open(filepath, 'rb') as f:
                    sample = f.read(sample_size)
                    lines_in_sample = sample.count(b'\n')
                    
                    if lines_in_sample > 0:
                        avg_line_size = sample_size / lines_in_sample
                        return int(file_size / avg_line_size)
                    return 0
        except:
            return 0
    
    def get_total_size(self) -> int:
        """Get total size of all databases"""
        total = 0
        for db in self.get_database_list():
            total += db['size']
        return total
    
    def show_database_info(self):
        """Show detailed database information"""
        databases = self.get_database_list()
        
        if RICH_AVAILABLE:
            self.console.print(Panel(
                "[bold cyan]DATABASE INFORMATION[/]",
                border_style="cyan"
            ))
            
            if not databases:
                self.console.print(Panel(
                    f"[yellow]No databases found in '{self.db_path}' folder[/]\n\n"
                    f"[white]Put your .txt or .csv files there to start searching[/]",
                    border_style="yellow"
                ))
                return
            
            # Create folder tree
            tree = Tree(f"[bold blue]{self.db_path}/[/]")
            folders = {}
            
            for db in databases:
                folder = db['folder']
                if folder not in folders:
                    if folder == '.':
                        folders[folder] = tree
                    else:
                        folders[folder] = tree.add(f"[blue]{folder}/[/]")
                
                size_str = self._format_size(db['size'])
                lines_str = f"{db['lines']:,}" if db['lines'] else "?"
                
                file_color = "green" if db['type'] == '.txt' else "yellow"
                folders[folder].add(
                    f"[{file_color}]{db['name']}[/] "
                    f"[dim]({size_str}, ~{lines_str} lines)[/]"
                )
            
            self.console.print(tree)
            
            # Summary table
            total_size = sum(db['size'] for db in databases)
            total_lines = sum(db['lines'] for db in databases if db['lines'])
            txt_count = len([db for db in databases if db['type'] == '.txt'])
            csv_count = len([db for db in databases if db['type'] == '.csv'])
            
            self.console.print()
            
            table = Table(title="SUMMARY", box=ROUNDED, border_style="cyan")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="green")
            
            table.add_row("Total Files", str(len(databases)))
            table.add_row("TXT Files", str(txt_count))
            table.add_row("CSV Files", str(csv_count))
            table.add_row("Total Size", self._format_size(total_size))
            table.add_row("Total Lines", f"~{total_lines:,}")
            table.add_row("Unique Folders", str(len(set(db['folder'] for db in databases))))
            
            self.console.print(table)
            
            # Top 5 largest files
            if len(databases) > 1:
                largest = sorted(databases, key=lambda x: x['size'], reverse=True)[:5]
                
                self.console.print()
                lg_table = Table(title="TOP 5 LARGEST FILES", box=ROUNDED, border_style="magenta")
                lg_table.add_column("#", style="dim", width=4)
                lg_table.add_column("File", style="cyan", width=35)
                lg_table.add_column("Size", style="yellow", width=12)
                lg_table.add_column("Lines", style="green", width=12)
                
                for i, db in enumerate(largest, 1):
                    lg_table.add_row(
                        str(i),
                        db['name'][:35],
                        self._format_size(db['size']),
                        f"~{db['lines']:,}" if db['lines'] else "?"
                    )
                
                self.console.print(lg_table)
        
        else:
            # Simple text output
            print("\n" + "=" * 70)
            print("                    DATABASE INFORMATION")
            print("=" * 70)
            
            if not databases:
                print(f"\n  [!] No databases found in '{self.db_path}' folder")
                print(f"  Put .txt or .csv files in this folder")
                print("\n" + "=" * 70)
                return
            
            # Group by folder
            folders = {}
            for db in databases:
                folder = db['folder']
                if folder not in folders:
                    folders[folder] = []
                folders[folder].append(db)
            
            total_size = 0
            total_files = 0
            
            for folder, files in sorted(folders.items()):
                print(f"\n  [FOLDER] {folder}/")
                
                for db in files:
                    size_str = self._format_size(db['size'])
                    lines_str = f"~{db['lines']:,}" if db['lines'] else "?"
                    print(f"     [{db['type'][1:].upper()}] {db['name']:<35} {size_str:>12}  {lines_str} lines")
                    total_size += db['size']
                    total_files += 1
            
            print("\n" + "-" * 70)
            print(f"  TOTAL: {total_files} files, {self._format_size(total_size)}")
            print("=" * 70)
    
    def _format_size(self, size_bytes: int) -> str:
        """Format file size for display"""
        if size_bytes >= 1024 ** 3:
            return f"{size_bytes / (1024 ** 3):.2f} GB"
        elif size_bytes >= 1024 ** 2:
            return f"{size_bytes / (1024 ** 2):.2f} MB"
        elif size_bytes >= 1024:
            return f"{size_bytes / 1024:.2f} KB"
        else:
            return f"{size_bytes} B"
    
    def validate_databases(self) -> Dict[str, Any]:
        """Validate database integrity"""
        results = {
            'valid': [],
            'errors': [],
            'warnings': [],
            'empty': []
        }
        
        for db in self.get_database_list():
            try:
                with open(db['path'], 'r', encoding='utf-8', errors='ignore') as f:
                    first_line = f.readline()
                    
                if first_line.strip():
                    results['valid'].append(db['name'])
                else:
                    results['empty'].append(db['name'])
                    
            except Exception as e:
                results['errors'].append(f"{db['name']}: {str(e)}")
        
        return results
    
    def analyze_file(self, filename: str) -> Dict[str, Any]:
        """Analyze specific database file"""
        for db in self.get_database_list():
            if db['name'] == filename:
                analysis = {
                    'name': db['name'],
                    'size': self._format_size(db['size']),
                    'lines': db['lines'],
                    'type': db['type'],
                    'modified': db['modified'].strftime('%Y-%m-%d %H:%M:%S'),
                    'sample_data': []
                }
                
                # Get sample lines
                try:
                    with open(db['path'], 'r', encoding='utf-8', errors='ignore') as f:
                        for i, line in enumerate(f):
                            if i >= 5:
                                break
                            analysis['sample_data'].append(line.strip()[:100])
                except:
                    pass
                
                return analysis
        
        return None
