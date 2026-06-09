<img width="569" height="536" alt="изображение" src="https://github.com/user-attachments/assets/3524f325-111a-4e7a-a8c9-c826fd1eb87c" /># PreOrder Service — система предзаказов товаров

[![CI](https://github.com/Hellondd/PreOrderService/actions/workflows/ci.yml/badge.svg)](https://github.com/Hellondd/PreOrderService/actions/workflows/ci.yml)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0.2-green.svg)](https://flask.palletsprojects.com/)

Сервис автоматизирует связку «потребность клиента — ожидаемая поставка». Позволяет бронировать дефицитный товар, находящийся в пути, исключая потерю прибыли из-за человеческого фактора. Уведомляет клиентов в Telegram о поступлении товара на склад.

---

## 📋 Функционал

- **Учёт транзитных поставок** – регистрация поставок со статусом «В пути» (In Transit)
- **Автоматическое бронирование** – при создании предзаказа проверяется доступный остаток в пути, резервируется товар
- **Лист ожидания (Waitlist)** – если товара в пути недостаточно, заказ попадает в лист ожидания и автоматически резервируется при поступлении новой поставки
- **Ролевая модель** – менеджер (admin) управляет поставками и приёмкой, клиент (client) создаёт предзаказы и привязывает Telegram ID
- **Telegram уведомления** – клиент получает сообщения о переводе заказа в статус «В пути» и о готовности к выдаче
- **Production‑готовность** – Docker Compose, GitHub Actions CI, Gunicorn, переменные окружения

---

## 🧰 Технологический стек

| Компонент       | Технологии                                                      |
|----------------|-----------------------------------------------------------------|
| Backend        | Python 3.11, Flask 3.0.2, Flask-SQLAlchemy                     |
| База данных    | SQLite (локально), для production рекомендуется PostgreSQL     |
| Интеграции     | Telegram Bot API, requests                                      |
| Тестирование   | pytest, coverage                                                |
| Качество кода  | flake8, black                                                   |
| Безопасность   | pip-audit, .env, .gitignore                                    |
| CI/CD          | GitHub Actions (проверка линтером, тесты, pip-audit)            |
| Контейнеризация| Docker, Docker Compose                                          |
| Веб-сервер     | Gunicorn (production)                                           |

---

## 🚀 Установка и запуск

### Требования
- Python 3.11 или выше
- Git
- (опционально) Docker и Docker Compose

### 1. Клонирование репозитория
```bash
git clone https://github.com/Hellondd/PreOrderService.git
cd PreOrderService
```
### 2. Настройка окружения

Скопируйте пример переменных окружения и отредактируйте под себя:
```

cp .env.example .env

Укажите в .env реальные значения:

    SECRET_KEY – секретный ключ Flask (сгенерируйте любой сложный)

    TELEGRAM_TOKEN – токен вашего Telegram-бота (получить у @BotFather)
```
3. Запуск локально (Windows)

Используйте готовые bat‑скрипты из папки scripts/:

``` cmd
scripts\setup.bat       # установка зависимостей
scripts\run.bat         # запуск приложения (по умолчанию http://127.0.0.1:5000)
```
Либо через командную строку:
```bash

pip install -r requirements.txt
python app.py
```
4. Запуск через Docker
```bash

docker compose up --build
```
Приложение будет доступно на http://localhost:5000.
Остановка: docker compose down.
5. Другие полезные скрипты

|Скрипт|	Назначение|
|----------------|-----------------------------------------------------------------|
|scripts\check.bat	|Запуск flake8 (линтер) без остановки при ошибках|
|scripts\format.bat	|Автоформатирование кода через black|
|scripts\test.bat	|Запуск pytest (тесты бизнес‑логики и API)|
|scripts\quality-check.bat	|Последовательный запуск линтера и тестов|
|scripts\backup.bat	|Создание резервной копии базы SQLite|
|scripts\restore.bat	|Восстановление базы из выбранного бэкапа|
|scripts\ports-check.bat	|Просмотр открытых портов|

🧪 Тестирование

Проект покрыт интеграционными тестами бизнес-логики (4 сценария) и API-тестами.

Запуск всех тестов:
```bash

pytest tests/ -v
```
Запуск с отчётом о покрытии:
```bash

pytest tests/ --cov=. --cov-report=html
```
⚙️ CI/CD (GitHub Actions)

При каждом push или pull request в ветки main, support/*, feature/* автоматически запускается workflow:

    Установка зависимостей

    Линтинг через flake8

    Тестирование через pytest

    Проверка уязвимостей зависимостей (pip-audit)

Статус сборки всегда отображается бейджем [CI] в начале README.
🔐 Переменные окружения

Файл .env (не загружается в репозиторий) должен содержать:
```

APP_ENV=production
APP_DEBUG=false
APP_HOST=0.0.0.0
APP_PORT=5000
DATABASE_URL=sqlite:///warehouse.db
SECRET_KEY=your_very_secret_key_here
TELEGRAM_TOKEN=your_bot_token_from_botfather
```
Примерный шаблон с пустыми значениями находится в .env.example.
📁 Структура проекта
```
text

PreOrderService/
├── .github/workflows/ci.yml   # CI конфигурация
├── modules/                   # Бизнес-логика
│   ├── identity.py            # аутентификация, хэширование
│   ├── inventory.py           # поставки, приёмка, обработка заказов
│   ├── orders.py              # создание предзаказов, расчёт остатков
│   └── notifications.py       # отправка Telegram-уведомлений
├── templates/                 # HTML-шаблоны (login, admin, client)
├── tests/                     # pytest тесты
├── scripts/                   # bat‑скрипты для Windows
├── docs/                      # документация этапов (отчёты, риски, changelog)
├── screenshots/               # скриншоты для отчётов
├── app.py                     # точка входа Flask
├── database.py                # модели SQLAlchemy
├── requirements.txt           # зависимости
├── docker-compose.yml         # контейнеризация
├── .env.example               # шаблон переменных окружения
├── .gitignore                 # исключённые файлы
├── CHANGELOG.md               # история изменений
├── RELEASE_NOTES.md           # описание релизов
└── README.md                  # этот файл
```
### Релизы

Актуальная стабильная версия: v0.2.0

    Исправлено логирование при отсутствии TELEGRAM_TOKEN

    Добавлены CHANGELOG и RELEASE NOTES

    Внедрён CI на GitHub Actions

Скачать архив релиза: Releases
### Внесение изменений

    Создайте issue с описанием проблемы или улучшения.

    Создайте ветку feature/... или support/....

    Внесите изменения, запустите локальные проверки (scripts\quality-check.bat).

    Убедитесь, что GitHub Actions проходит зелёным.

    Оформите Pull Request с ссылкой на issue.

    После слияния обновите CHANGELOG.md и при необходимости создайте новый релиз.

### Скриншоты работы проекта.
<img width="1599" height="617" alt="изображение" src="https://github.com/user-attachments/assets/e01e197d-7e24-470d-bd22-52ead4afc015" />
Окно пользователя<br>
<img width="1469" height="513" alt="изображение" src="https://github.com/user-attachments/assets/3b2a6b16-7d39-4291-bbb7-909df78c9282" />
Окно админа<br>

<img width="569" height="536" alt="изображение" src="https://github.com/user-attachments/assets/cb5e82d9-6c03-46ad-8789-3f7fb9a5e5e1" /><br>
Окно авторизации
