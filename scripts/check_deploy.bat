@echo off
chcp 65001 > nul
echo Проверка доступности публичного URL...
curl -I https://preorderservice.onrender.com
