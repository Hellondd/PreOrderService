@echo off
chcp 65001 > nul
cd /d "%~dp0\.."

echo ========================================
echo Запуск pytest с отчетом о покрытии
echo ========================================

REM Запуск тестов и сохранение результатов в файл
pytest tests/ -v --tb=short --cov=. --cov-report=html --cov-report=term > reports/pytest_report.txt 2>&1

echo.
echo Тесты завершены. Отчеты сохранены в:
echo - reports/pytest_report.txt
echo - htmlcov/index.html (покрытие кода)
echo.
pause