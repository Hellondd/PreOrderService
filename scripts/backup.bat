@echo off
chcp 65001 > nul
cd /d "%~dp0\.."
if not exist backups mkdir backups
set timestamp=%date:~6,4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%
copy warehouse.db backups\backup_%timestamp%.db
echo Backup created: backups\backup_%timestamp%.db
pause