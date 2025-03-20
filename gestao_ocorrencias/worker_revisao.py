import os
import sys
import time
import django
from datetime import datetime
from django.core.management import call_command

# 📌 **🔹 GARANTIR O CAMINHO CORRETO DO PROJETO DJANGO**
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
sys.path.append(PROJECT_DIR)

# 📌 **🔹 CONFIGURAR O DJANGO CORRETAMENTE**
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gestao_ocorrencias.settings")

try:
    django.setup()
except Exception as e:
    print(f"❌ Erro ao inicializar Django: {e}")
    sys.exit(1)

def esperar_ate_horario():
    """🕒 Aguarda até 01:00 antes de rodar a revisão de ocorrências."""
    print("🚀 Worker de Revisão iniciado! Aguardando horário correto...")

    while True:
        agora = datetime.now().strftime("%H:%M")

        print(f"🔍 [DEBUG] Agora: {agora} | Horário programado: 01:00")

        if agora == "01:00":
            print(f"🕒 {agora} - Iniciando revisão de ocorrências...")
            try:
                call_command("revisar_ocorrencias")
                print("✅ Revisão de ocorrências concluída com sucesso!")
            except Exception as e:
                print(f"❌ Erro ao revisar ocorrências: {e}")

            time.sleep(86400)  # Aguarda 24h até a próxima execução
        else:
            print("⏳ Ainda não é a hora, aguardando 30 segundos...")
            time.sleep(30)

if __name__ == "__main__":
    esperar_ate_horario()
