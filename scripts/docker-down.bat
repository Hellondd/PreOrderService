@echo off
chcp 65001 > nul
cd /d "%~dp0\.."

echo ========================================
echo  Остановка контейнеров Docker
echo ========================================
docker compose down