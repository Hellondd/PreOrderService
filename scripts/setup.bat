@echo off
chcp 65001 > nul
cd /d "%~dp0\.."

echo ========================================
echo  Установка зависимостей
echo ========================================
pip install -r requirements.txt