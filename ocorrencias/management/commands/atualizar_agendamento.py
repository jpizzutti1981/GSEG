import os
from django.core.management.base import BaseCommand
from ocorrencias.models import Agendamento

class Command(BaseCommand):
    help = "Atualiza os agendamentos no sistema"

    def handle(self, *args, **kwargs):
        agendamentos = Agendamento.objects.filter(ativo=True)  # Filtra os agendamentos ativos
        
        if not agendamentos.exists():
            self.stdout.write(self.style.WARNING("Nenhum agendamento ativo encontrado."))
            return
        
        for agendamento in agendamentos:
            hora = agendamento.horario.hour
            minuto = agendamento.horario.minute

            # Comando para rodar o script de envio da sinopse no horário desejado
            comando = f"{minuto} {hora} * * * /caminho/para/python /caminho/do/projeto/manage.py enviar_sinopse"

            # Adiciona o comando ao cron (Linux/macOS)
            os.system(f'(crontab -l; echo "{comando}") | crontab -')

        self.stdout.write(self.style.SUCCESS("Agendamento atualizado no sistema!"))
