import requests
import os
from django.conf import settings
from reportlab.lib.pagesizes import letter  # import faltante do tamanho padrão do PDF
from reportlab.pdfgen import canvas
import io
import os
from django.template.loader import render_to_string
from weasyprint import HTML
from django.conf import settings
from django.template.loader import render_to_string
import os
import io
from django.conf import settings
from django.template.loader import render_to_string
from weasyprint import HTML
import os
import io
from django.conf import settings
from django.template.loader import render_to_string
from weasyprint import HTML
import locale

import os
import io
import unicodedata
from django.conf import settings
from django.template.loader import render_to_string
from weasyprint import HTML


TELEGRAM_BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID = settings.TELEGRAM_CHAT_ID

def enviar_mensagem_telegram(mensagem, imagem_caminho=None):
    url_mensagem = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    dados_mensagem = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensagem,
        "parse_mode": "HTML",
    }

    # 🔹 Enviar mensagem de texto
    response = requests.post(url_mensagem, json=dados_mensagem)

    # 🔹 Enviar imagem, se fornecida
    if imagem_caminho:
        url_imagem = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"

        if imagem_caminho.startswith("http"):  # 🌐 Se for URL (Cloudinary)
            requests.post(url_imagem, data={"chat_id": TELEGRAM_CHAT_ID, "photo": imagem_caminho})
        
        else:  # 📂 Se for arquivo local
            imagem_path = os.path.join(settings.MEDIA_ROOT, imagem_caminho)
            if os.path.exists(imagem_path):
                with open(imagem_path, 'rb') as imagem:
                    requests.post(url_imagem, data={"chat_id": TELEGRAM_CHAT_ID}, files={"photo": imagem})

# 🔹 Configura para português (Brasil)
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except locale.Error:
    locale.setlocale(locale.LC_TIME, 'C')  # Fallback para um formato padrão



def remover_acentos(texto):
    """ Remove acentos e caracteres especiais para um nome de arquivo seguro. """
    return ''.join(c for c in unicodedata.normalize('NFKD', texto) if unicodedata.category(c) != 'Mn')

def gerar_pdf_notificacao(notificacao):
    """ Gera um PDF profissional da notificação """

    # 🔹 Caminho correto dos logos (mantém local)
    logo_esquerda_path = os.path.join(settings.BASE_DIR, "static", "images", "logo.png")
    logo_direita_path = os.path.join(settings.BASE_DIR, "static", "images", "logoad3.png")

    # 🔹 Usa a URL pública do Cloudinary se a imagem foi enviada para lá
    imagem_ocorrencia_url = notificacao.imagem.url if notificacao.imagem else None

    # 🔹 Verifica se os logos existem antes de carregar
    if not os.path.exists(logo_esquerda_path):
        print("❌ Erro: Logo Pontal NÃO encontrado!")
        logo_esquerda_path = None
    if not os.path.exists(logo_direita_path):
        print("❌ Erro: Logo AD Shopping NÃO encontrado!")
        logo_direita_path = None

    # 🔹 Formatar nome do arquivo (evita caracteres inválidos)
    loja_formatada = notificacao.loja.replace(" ", "_")
    meses = {
        "01": "Janeiro", "02": "Fevereiro", "03": "Março", "04": "Abril",
        "05": "Maio", "06": "Junho", "07": "Julho", "08": "Agosto",
        "09": "Setembro", "10": "Outubro", "11": "Novembro", "12": "Dezembro"
    }
    data_ocorrencia = notificacao.data_ocorrencia.strftime('%d/%m/%Y')
    dia, mes, ano = data_ocorrencia.split('/')
    data_formatada = f"{dia}_{mes}_{ano}"
    data_formatada_extenso = f"{dia} de {meses[mes]} de {ano}"

    pdf_filename = f"{loja_formatada}_{data_formatada}.pdf"

    # 🔹 Caminho para salvar o PDF (mantém local)
    pdf_path = os.path.join(settings.MEDIA_ROOT, "notificacoes", pdf_filename)

    # 🔹 Renderiza o HTML para PDF com a URL correta da imagem
    html_content = render_to_string("notificacoes/notificacao_pdf.html", {
        "notificacao": notificacao,
        "logo_esquerda": f"file:///{logo_esquerda_path.replace(os.sep, '/')}" if logo_esquerda_path else None,
        "logo_direita": f"file:///{logo_direita_path.replace(os.sep, '/')}" if logo_direita_path else None,
        "imagem_ocorrencia": imagem_ocorrencia_url,  # 🔹 Usa a URL pública do Cloudinary
        "data_formatada_extenso": data_formatada_extenso  # 🔹 Envia a data formatada para o HTML
    })

    # 🔹 Converte HTML para PDF
    pdf_file = io.BytesIO()
    HTML(string=html_content, base_url=settings.BASE_DIR).write_pdf(pdf_file)

    # 🔹 Salva o PDF no diretório correto
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    with open(pdf_path, "wb") as f:
        f.write(pdf_file.getvalue())

    return pdf_path
