import os
import time
from datetime import datetime
from django.core.cache import cache
from django.core.management import call_command
import django

# Configurar Django para rodar no Worker
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gestao_ocorrencias.settings")
django.setup()

def esperar_ate_horario():
    """🕒 Aguarda até o horário correto antes de enviar a sinopse."""
    print("🚀 Worker iniciado! Aguardando horário correto...")

    while True:
        # 📌 Obtém o horário de envio atualizado do cache ou usa um padrão
        horario_envio = cache.get("HORARIO_ENVIO", "23:30")
        agora = datetime.now().strftime("%H:%M")

        if agora == horario_envio:
            print(f"🕒 {agora} - Enviando sinopse...")
            try:
                call_command("enviar_sinopse")
                print("✅ Sinopse enviada com sucesso!")
            except Exception as e:
                print(f"❌ Erro ao enviar sinopse: {e}")

            time.sleep(86400)  # Aguarda 24h até a próxima execução

        else:
            time.sleep(30)  # Verifica a cada 30 segundos se chegou a hora

if __name__ == "__main__":
    esperar_ate_horario()
