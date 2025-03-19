import os
from django.core.management.base import BaseCommand
from ocorrencias.models import ConfiguracaoAutomacao

class Command(BaseCommand):
    help = "Atualiza o cron job para envio da Sinopse"

    def handle(self, *args, **kwargs):
        config = ConfiguracaoAutomacao.objects.first()
        if not config:
            self.stdout.write(self.style.ERROR("⚠ Nenhuma configuração encontrada."))
            return

        # 🔹 Obtém horário salvo no banco
        hora, minuto = config.horario_envio.strftime("%H"), config.horario_envio.strftime("%M")

        # 🔹 Define o comando cron para rodar no horário especificado
        cron_job = f"{minuto} {hora} * * * /home/render/project/src/scripts/enviar_sinopse.sh\n"

        # 🔹 Atualiza o crontab do sistema
        os.system(f'(crontab -l; echo "{cron_job}") | crontab -')

        self.stdout.write(self.style.SUCCESS(f"✅ Cron job atualizado para {config.horario_envio}"))
