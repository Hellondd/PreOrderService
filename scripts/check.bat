@echo off
chcp 65001 > nul
cd /d "%~dp0\.."

echo ========================================
echo  Проверка кода линтером (flake8)
echo ========================================
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=120 --statistics