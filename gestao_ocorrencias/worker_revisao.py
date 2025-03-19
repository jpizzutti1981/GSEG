import os
import sys
import time
import django
from datetime import datetime
from django.core.management import call_command
from django.core.cache import cache

# 📌 **🔹 GARANTIR O CAMINHO CORRETO DO PROJETO DJANGO**
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
sys.path.append(PROJECT_DIR)  # 🔹 Adiciona o diretório do projeto ao `sys.path`

# 📌 **🔹 CONFIGURAR O DJANGO CORRETAMENTE**
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gestao_ocorrencias.settings")

try:
    django.setup()
except Exception as e:
    print(f"❌ Erro ao inicializar Django: {e}")
    sys.exit(1)

def esperar_ate_horario():
    """🕒 Aguarda até 01h para revisar ocorrências automaticamente."""
    print("🚀 Worker de Revisão iniciado! Aguardando horário correto...")

    while True:
        # 📌 Obtém o horário programado
        horario_programado = "01:00"  # 🔹 Sempre rodar às 01h
        agora = datetime.now().strftime("%H:%M")

        print(f"🔍 [DEBUG] Agora: {agora} | Horário programado: {horario_programado}")

        if agora == horario_programado:
            print(f"🕒 {agora} - Revisando ocorrências...")
            try:
                call_command("revisar_ocorrencias")
                print("✅ Revisão de ocorrências concluída com sucesso!")
            except Exception as e:
                print(f"❌ Erro ao revisar ocorrências: {e}")

            time.sleep(86400)  # 🔹 Espera 24 horas para rodar novamente

        else:
            print("⏳ Ainda não é a hora, aguardando 60 segundos...")
            time.sleep(60)  # 🔹 Verifica a cada 1 minuto se chegou a hora

if __name__ == "__main__":
    esperar_ate_horario()
