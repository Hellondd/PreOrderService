import requests
import logging

# Настройка базового логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NotificationModule:
    BOT_TOKEN = "8624343638:AAHuXapkVVDMYE9K7o-RDipJN_QleOHCFRM" 

    @staticmethod
    def send_telegram_msg(chat_id, text):
        if not chat_id:
            return
        
        url = f"https://api.telegram.org/bot{NotificationModule.BOT_TOKEN}/sendMessage"
        payload = {"chat_id": chat_id, "text": text}
        try:
            response = requests.post(url, json=payload, timeout=5)
            response.raise_for_status() # Выбросит исключение при HTTP ошибке (например, 403)
        except requests.exceptions.RequestException as e:
            logging.error(f"Сетевая ошибка при отправке Telegram-уведомления на ID {chat_id}: {e}")