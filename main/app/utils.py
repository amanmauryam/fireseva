import requests
from django.conf import settings


def send_telegram_message(message):

    token = settings.TELEGRAM_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    data = {
        "chat_id": chat_id,
        "text": message
    }

    requests.post(url, data=data)



import re
from bs4 import BeautifulSoup


def generate_faq_schema(html):
    if not html:
        return None

    soup = BeautifulSoup(html, "html.parser")

    faq = []

    questions = soup.find_all("h3")

    for q in questions:
        answer = q.find_next("p")

        if answer:
            faq.append({
                "@type": "Question",
                "name": q.get_text(strip=True),
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": answer.get_text(" ", strip=True)
                }
            })

    if not faq:
        return None

    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": faq
    }    