# Развертывание в Production (PaaS)

## 1. Где развернут проект
Вариант: B. PaaS / GitHub deploy (Render.com)
Адрес: (https://preorderservice.onrender.com)

## 2. Требования
- Автоматическая сборка: GitHub Actions / Render CI
- Зависимости: Python 3.10, Gunicorn
- Переменные окружения: `SECRET_KEY`, `TELEGRAM_TOKEN`, `PYTHON_VERSION=3.10.0`

## 3. Команды развертывания (Настройки PaaS)
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`

## 4. Проверка и управление
- Адрес приложения: `https://preorderservice.onrender.com`
- Логи доступны во вкладке "Logs" в панели управления Render.
- Перезапуск сервиса (Manual Deploy -> Restart Service).
