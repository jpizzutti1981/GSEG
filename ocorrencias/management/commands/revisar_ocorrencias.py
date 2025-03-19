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
    """🕒 Aguarda até o horário correto antes de revisar ocorrências."""
    print("🚀 Worker de Revisão de Ocorrências iniciado! Aguardando horário correto...")

    while True:
        # 📌 Obtém o horário de revisão do cache ou usa um padrão
        horario_revisao = cache.get("HORARIO_REVISAO", "01:00")
        agora = datetime.now().strftime("%H:%M")

        print(f"🔍 [DEBUG] Agora: {agora} | Horário programado: {horario_revisao}")

        if agora == horario_revisao:
            print(f"🕒 {agora} - Iniciando revisão de ocorrências...")
            try:
                call_command("revisar_ocorrencias")
                print("✅ Revisão de ocorrências concluída com sucesso!")
            except Exception as e:
                print(f"❌ Erro ao revisar ocorrências: {e}")

            time.sleep(86400)  # Aguarda 24h até a próxima execução

        else:
            print("⏳ Ainda não é a hora, aguardando 30 segundos...")
            time.sleep(30)  # Verifica a cada 30 segundos se chegou a hora

if __name__ == "__main__":
    esperar_ate_horario()
