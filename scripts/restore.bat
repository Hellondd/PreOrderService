@echo off
chcp 65001 > nul
cd /d "%~dp0\.."
echo Available backups:
dir backups\*.db
set /p file="Enter backup filename (e.g., backup_20260609_1430.db): "
copy backups\%file% warehouse.db /Y
echo Restored. Restart the app.
pause