import requests
import os
from django.conf import settings

TELEGRAM_BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID = settings.TELEGRAM_CHAT_ID

def enviar_mensagem_telegram(mensagem, imagem_url=None):
    url_mensagem = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    
    dados_mensagem = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": mensagem,
        "parse_mode": "HTML",
    }

    # Envia a mensagem de texto primeiro
    response = requests.post(url_mensagem, json=dados_mensagem)

    # Se houver imagem, enviar a foto
    if imagem_url:
        url_imagem = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendPhoto"
        
        dados_imagem = {
            "chat_id": settings.TELEGRAM_CHAT_ID,
            "photo": imagem_url  # Aqui enviamos a URL pública
        }

        resposta_imagem = requests.post(url_imagem, json=dados_imagem)
        print(resposta_imagem.json())  # Debug: veja a resposta do Telegram no terminal