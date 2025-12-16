@echo off
chcp 65001 >nul 2>&1
title Index Databases

echo.
echo ============================================================
echo            INDEXING DATABASES
echo ============================================================
echo.
echo [*] Indexing all files in "bd" folder...
echo.

python -c "from modules.file_indexer import FileIndexer; from modules.config_manager import ConfigManager; from modules.logger import Logger; c=ConfigManager(); l=Logger(c); i=FileIndexer(c,l); i.index_all_databases(); s=i.get_stats(); print('Done! Files: ' + str(s.get('files',0)) + ', Records: ' + str(s.get('records',0)))"

echo.
pause
