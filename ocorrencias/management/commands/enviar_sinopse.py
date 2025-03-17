import os
from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from django.conf import settings
from ocorrencias.models import ConfiguracaoAutomacao
from datetime import datetime, timedelta
from ocorrencias.views import gerar_sinopse_pdf  # 🔹 Importação correta

class Command(BaseCommand):
    help = "Envia a Sinopse Diária por e-mail com anexo"

    def handle(self, *args, **kwargs):
        config = ConfiguracaoAutomacao.objects.first()
        if not config:
            self.stdout.write(self.style.ERROR("Erro: Nenhuma configuração de e-mail encontrada."))
            return

        data_ontem = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        data_ontem_formatada = (datetime.today() - timedelta(days=1)).strftime("%d/%m/%Y")
        data_nome_arquivo = (datetime.today() - timedelta(days=1)).strftime("%d-%m-%Y")

        emails_destinatarios = [email.strip() for email in config.emails_destinatarios.split(",") if email.strip()]
        if not emails_destinatarios:
            self.stdout.write(self.style.ERROR("Erro: Nenhum destinatário configurado."))
            return

        assunto = f"Sinopse Diária - {data_ontem_formatada}"
        mensagem = f"Segue, anexo, a sinopse diária do dia {data_ontem_formatada}."

        # **🚀 Geração do PDF agora retorna um caminho de arquivo válido**
        caminho_pdf = gerar_sinopse_pdf(None, data_ontem, data_ontem)  

        if not os.path.exists(caminho_pdf):
            self.stdout.write(self.style.ERROR(f"Erro: O arquivo PDF '{caminho_pdf}' não foi encontrado."))
            return

        email = EmailMessage(
            subject=assunto,
            body=mensagem,
            from_email=settings.EMAIL_HOST_USER,
            to=emails_destinatarios
        )
        email.attach_file(caminho_pdf)

        try:
            email.send()
            self.stdout.write(self.style.SUCCESS(f"Sinopse enviada com sucesso: {caminho_pdf}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erro ao enviar e-mail: {str(e)}"))
