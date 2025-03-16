import os
import requests
from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand
from controle_chaves.models import MovimentacaoChave

class Command(BaseCommand):
    help = "Envia relatório de chaves não devolvidas no Telegram"

    def handle(self, *args, **kwargs):
        # 🔹 Pega as configurações do `settings.py`
        TELEGRAM_BOT_TOKEN = getattr(settings, "TELEGRAM_BOT_TOKEN", None)
        TELEGRAM_CHAT_ID = getattr(settings, "TELEGRAM_CHAT_ID", None)

        if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
            self.stdout.write(self.style.ERROR("❌ Configurações do Telegram não encontradas no settings.py"))
            return

        agora = datetime.now().strftime("%d/%m/%Y %H:%M")
        chaves_nao_devolvidas = MovimentacaoChave.objects.filter(status="Não Devolvida")

        if not chaves_nao_devolvidas.exists():
            self.stdout.write(self.style.SUCCESS("✅ Nenhuma chave pendente."))
            return

        mensagem = f"📢 *Relatório de Chaves Não Devolvidas* \n📅 {agora}\n\n"
        for chave in chaves_nao_devolvidas:
            mensagem += (
                f"🔑 *Chave:* {chave.chave.numero} - {chave.chave.nome}\n"
                f"👤 *Responsável:* {chave.responsavel}\n"
                f"📞 *Telefone:* {chave.telefone}\n"
                f"📆 *Data Saída:* {chave.data_saida}\n"
                f"🕒 *Horário Saída:* {chave.horario_saida}\n\n"
            )

        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": mensagem,
            "parse_mode": "Markdown"
        }

        try:
            response = requests.post(url, data=payload)
            if response.status_code == 200:
                self.stdout.write(self.style.SUCCESS("📨 Relatório enviado com sucesso!"))
            else:
                self.stdout.write(self.style.ERROR(f"❌ Erro ao enviar relatório: {response.text}"))
        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f"❌ Falha na requisição: {e}"))
