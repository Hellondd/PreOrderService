import requests

class NotificationModule:
    BOT_TOKEN = "8624343638:AAHuXapkVVDMYE9K7o-RDipJN_QleOHCFRM" 

    @staticmethod
    def send_telegram_msg(chat_id, text):
        if not chat_id:
            return # Если ID не указан, игнорируем
        
        url = f"https://api.telegram.org/bot{NotificationModule.BOT_TOKEN}/sendMessage"
        payload = {"chat_id": chat_id, "text": text}
        try:
            requests.post(url, json=payload, timeout=5)
        except Exception as e:
            print(f"Ошибка отправки Telegram-уведомления: {e}")