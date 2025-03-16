from django.core.management.base import BaseCommand
from ocorrencias.models import Ocorrencia
from datetime import datetime

class Command(BaseCommand):
    help = 'Corrige os horários inválidos no banco de dados'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("🔍 Iniciando a correção dos horários..."))

        ocorrencias = Ocorrencia.objects.all()
        for ocorrencia in ocorrencias:
            if isinstance(ocorrencia.horario, str):  # Se o horário estiver salvo incorretamente como string
                try:
                    ocorrencia.horario = datetime.strptime(ocorrencia.horario, "%H:%M").time()
                    ocorrencia.save()
                    self.stdout.write(self.style.SUCCESS(f'✔️ Corrigido: {ocorrencia.id}'))
                except ValueError:
                    self.stdout.write(self.style.ERROR(f'❌ Erro na ocorrência {ocorrencia.id}, verificar manualmente'))
        
        self.stdout.write(self.style.SUCCESS("✅ Correção concluída!"))
