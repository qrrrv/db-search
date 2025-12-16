#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DATABASE SEARCH TOOL v2.0 PRO
With 15 Animated Themes
"""

import os
import sys
import time

# Fix path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

# Import modules
try:
    from modules.search_engine import SearchEngine
    from modules.ui_manager import UIManager
    from modules.config_manager import ConfigManager
    from modules.logger import Logger
    from modules.file_indexer import FileIndexer
    from modules.result_exporter import ResultExporter
    from modules.stats_manager import StatsManager
    from modules.cache_manager import CacheManager
    from modules.parallel_processor import ParallelProcessor
    from modules.database_manager import DatabaseManager
    
    MODULES_LOADED = True
except ImportError as e:
    MODULES_LOADED = False
    IMPORT_ERROR = str(e)


def check_modules():
    """Check if all modules are available"""
    if not MODULES_LOADED:
        print(f"[ERROR] Cannot import module: {IMPORT_ERROR}")
        print(f"[INFO] Script directory: {SCRIPT_DIR}")
        print(f"[INFO] Checking modules folder...")
        
        modules_path = os.path.join(SCRIPT_DIR, 'modules')
        if os.path.exists(modules_path):
            print(f"[OK] Modules folder exists")
            files = os.listdir(modules_path)
            print(f"[INFO] Files in modules: {files}")
            
            required = [
                'search_engine.py', 'ui_manager.py', 'config_manager.py',
                'logger.py', 'file_indexer.py', 'result_exporter.py',
                'stats_manager.py', 'cache_manager.py', 'parallel_processor.py',
                'database_manager.py'
            ]
            
            missing = [f for f in required if f not in files]
            if missing:
                print(f"[ERROR] Missing files: {missing}")
        else:
            print(f"[ERROR] Modules folder not found!")
        
        input("\nPress Enter to exit...")
        sys.exit(1)


def main():
    """Main function"""
    check_modules()
    
    try:
        # Initialize components
        config = ConfigManager()
        logger = Logger(config)
        ui = UIManager(config)
        
        # Clear screen and show banner
        ui.clear_screen()
        ui.show_banner()
        
        # Initialize managers
        cache = CacheManager(config)
        db_manager = DatabaseManager(config, logger)
        indexer = FileIndexer(config, logger)
        processor = ParallelProcessor(config, logger)
        exporter = ResultExporter(config, logger)
        stats = StatsManager(config, logger)
        
        # Create search engine
        search_engine = SearchEngine(
            config=config,
            logger=logger,
            cache=cache,
            indexer=indexer,
            processor=processor,
            db_manager=db_manager
        )
        
        # Main loop
        while True:
            ui.show_menu()
            choice = ui.get_user_choice()
            
            if choice == '1':
                # Search in databases
                ui.clear_screen()
                ui.show_search_header()
                query = ui.get_search_query()
                
                if query:
                    start_time = time.time()
                    ui.show_progress_start()
                    
                    try:
                        results = search_engine.search(query)
                        duration = time.time() - start_time
                        
                        ui.show_progress_stop(success=True)
                        ui.show_results(results, stats)
                        
                        # Record in statistics
                        stats.record_search(query, len(results), duration)
                        
                        if results and ui.ask_export():
                            filepath = exporter.export(results, query)
                            ui.show_export_success(filepath)
                    except Exception as e:
                        ui.show_progress_stop(success=False)
                        ui.show_error(str(e))
                        
            elif choice == '2':
                # Index databases
                ui.clear_screen()
                ui.show_indexing_header()
                indexer.index_all_databases()
                ui.show_indexing_complete(indexer.get_stats())
                
            elif choice == '3':
                # Statistics
                ui.clear_screen()
                stats.show_statistics()
                
                # Show cache stats
                cache_stats = cache.get_stats()
                print(f"\n  Cache:")
                print(f"     Entries: {cache_stats['entries']}")
                print(f"     Hit rate: {cache_stats['hit_rate']}")
                
            elif choice == '4':
                # Settings
                ui.clear_screen()
                config.interactive_settings(ui)
                
            elif choice == '5':
                # Clear cache
                cache.clear()
                ui.show_cache_cleared()
                
            elif choice == '6':
                # Database info
                ui.clear_screen()
                db_manager.show_database_info()
                
            elif choice == '7':
                # Change theme with animation
                ui.clear_screen()
                new_theme = ui.show_theme_selector()
                ui.set_theme(new_theme)
                ui.clear_screen()
                ui.show_banner()
                
            elif choice == '0' or choice.lower() == 'q':
                ui.show_goodbye()
                break
                
            else:
                ui.show_invalid_choice()
                
            ui.wait_for_key()
            ui.clear_screen()
            ui.show_banner()
            
    except KeyboardInterrupt:
        print("\n\n[!] Program interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] Critical error: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
        sys.exit(1)


if __name__ == "__main__":
    main()