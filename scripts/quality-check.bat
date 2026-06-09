@echo off
chcp 65001 > nul
cd /d "%~dp0\.."
echo ========================================
echo Общая проверка качества проекта
echo ========================================
call scripts\check.bat
call scripts\test.bat
echo Проверка завершена.