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
        # 🔹 Buscar configuração do e-mail
        config = ConfiguracaoAutomacao.objects.first()
        
        if not config:
            self.stdout.write(self.style.ERROR("Erro: Nenhuma configuração de e-mail encontrada."))
            return

        # 🔹 Define a data do dia anterior
        data_ontem = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        data_ontem_formatada = (datetime.today() - timedelta(days=1)).strftime("%d/%m/%Y")
        data_nome_arquivo = (datetime.today() - timedelta(days=1)).strftime("%d-%m-%Y")  # 🔹 Nome DD-MM-YYYY

        # 🔹 Prepara os dados do e-mail
        emails_destinatarios = [email.strip() for email in config.emails_destinatarios.split(",") if email.strip()]
        if not emails_destinatarios:
            self.stdout.write(self.style.ERROR("Erro: Nenhum destinatário configurado."))
            return

        assunto = f"Sinopse Diária - {data_ontem_formatada}"
        mensagem = f"Segue, anexo, a sinopse diária do dia {data_ontem_formatada}."

        # 🔹 Gerar o PDF da sinopse antes do envio
        caminho_pdf = gerar_sinopse_pdf(None, data_ontem, data_ontem)  # 🔹 Chamada correta

        # 🔹 Verifica se o PDF foi gerado corretamente antes de anexar
        if not isinstance(caminho_pdf, str) or not os.path.exists(caminho_pdf):
            self.stdout.write(self.style.ERROR(f"Erro: O arquivo PDF '{caminho_pdf}' não foi encontrado."))
            return

        # 🔹 Criar e-mail com anexo
        email = EmailMessage(
            subject=assunto,
            body=mensagem,
            from_email=settings.EMAIL_HOST_USER,
            to=emails_destinatarios
        )
        email.attach_file(caminho_pdf)  # 🔹 Anexa o PDF gerado

        # 🔹 Enviar e-mail
        try:
            email.send()
            self.stdout.write(self.style.SUCCESS(f"Sinopse enviada com sucesso com anexo: Sinopse_Diária_{data_nome_arquivo}.pdf"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erro ao enviar e-mail: {str(e)}"))
