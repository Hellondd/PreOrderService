@echo off
chcp 65001 > nul
cd /d "%~dp0\.."

echo ========================================
echo  Запуск контейнеров Docker
echo ========================================
docker compose up --build