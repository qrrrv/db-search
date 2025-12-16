@echo off
chcp 65001 >nul 2>&1
title Quick Search - DB Search Tool

echo.
echo ============================================================
echo            QUICK SEARCH
echo ============================================================
echo.

set /p query="Enter search query: "

if "%query%"=="" (
    echo [ERROR] Query cannot be empty
    pause
    exit /b 1
)

python -c "from modules.search_engine import SearchEngine; from modules.config_manager import ConfigManager; from modules.logger import Logger; from modules.cache_manager import CacheManager; from modules.file_indexer import FileIndexer; from modules.parallel_processor import ParallelProcessor; from modules.database_manager import DatabaseManager; c=ConfigManager(); l=Logger(c); s=SearchEngine(c,l,CacheManager(c),FileIndexer(c,l),ParallelProcessor(c,l),DatabaseManager(c,l)); r=s.search('%query%'); print('Found: ' + str(len(r)) + ' results'); [print('[' + str(i+1) + '] ' + str(x.get('file','')) + ': ' + str(x.get('raw_data',''))[:80]) for i,x in enumerate(r[:20])]"

echo.
pause
