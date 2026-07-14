import requests


def send_telegram_message(message):

    token = "8879120181:AAHNXAkhYkrZvtX0o-OyzEg3NYNs_M5JCGI"
    chat_id = 763062252

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    data = {
        "chat_id": chat_id,
        "text": message
    }

    requests.post(url, data=data)