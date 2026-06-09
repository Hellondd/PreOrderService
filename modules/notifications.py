import requests
import logging
import os

# Настройка базового логирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class NotificationModule:
    BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
    IS_DEBUG = os.getenv("DEBUG", "False") == "True"

    @staticmethod
    def send_telegram_msg(chat_id, text):
        if not chat_id:
            logging.warning("Telegram chat_id is empty, notification skipped")
            return
        if not NotificationModule.BOT_TOKEN:
            logging.warning("TELEGRAM_TOKEN is not set. Set it in .env to enable notifications.")
            return

        if NotificationModule.IS_DEBUG:
            logging.info(f"DEBUG: Отправка сообщения на {chat_id}: {text}")

        url = f"https://api.telegram.org/bot{NotificationModule.BOT_TOKEN}/sendMessage"
        payload = {"chat_id": chat_id, "text": text}
        try:
            response = requests.post(url, json=payload, timeout=5)
            response.raise_for_status()
        except requests.exceptions.Timeout:
            logging.error(
                f"Ошибка отладки: Превышено время ожидания API для ID {chat_id}"
            )
        except requests.exceptions.RequestException as e:
            logging.error(
                f"Сетевая ошибка при отправке Telegram-уведомления на ID {chat_id}: {e}"
            )
