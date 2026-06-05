# Инструкция по установке и запуску (PreOrder Service)

## Локальный запуск (Windows)
1. Установите зависимости: `scripts\setup.bat`
2. Запустите проект: `scripts\run.bat`
3. Сервис будет доступен по адресу: `http://127.0.0.1:5000`

## Запуск через Docker
1. Поднимите контейнеры: `scripts\docker-up.bat` (или `make docker-up`)
2. Для остановки сервиса: `scripts\docker-down.bat` (или `make docker-down`)
3. Просмотр логов: `scripts\logs.bat` (или `make logs`)

## Инструменты разработчика
* Проверка качества кода: `scripts\check.bat` (или `make check`)
* Автоформатирование: `scripts\format.bat` (или `make format`)