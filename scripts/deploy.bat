@echo off
chcp 65001 > nul
cd /d "%~dp0\.."
echo Запуск деплоя на PaaS через отправку изменений в ветку main...
git add .
git commit -m "deploy: trigger production build"
git push origin main
echo Деплой инициирован. Проверьте дашборд Render.