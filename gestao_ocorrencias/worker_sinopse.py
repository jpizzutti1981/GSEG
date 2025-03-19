import os
import sys
import time
import django
from datetime import datetime
from django.core.management import call_command

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

from ocorrencias.models import ConfiguracaoAutomacao  # 🔹 Importação do modelo

def obter_horario_envio():
    """🔹 Busca o horário atualizado do banco de dados"""
    config = ConfiguracaoAutomacao.objects.first()
    if config and config.horario_envio:
        return config.horario_envio.strip()
    return "23:30"  # 🔹 Se não houver configuração, usa um padrão

def esperar_ate_horario():
    """🕒 Aguarda até o horário correto antes de enviar a sinopse."""
    print("🚀 Worker iniciado! Aguardando horário correto...")

    while True:
        horario_envio = obter_horario_envio()  # 🔹 Agora busca direto do banco de dados
        agora = datetime.now().strftime("%H:%M")

        print(f"🔍 [DEBUG] Agora: {agora} | Horário programado: {horario_envio}")

        if agora == horario_envio:
            print(f"🕒 {agora} - Enviando sinopse...")
            try:
                call_command("enviar_sinopse")
                print("✅ Sinopse enviada com sucesso!")
            except Exception as e:
                print(f"❌ Erro ao enviar sinopse: {e}")

            time.sleep(61)  # 🔹 Aguarda 61 segundos antes de verificar novamente

        else:
            print("⏳ Ainda não é a hora, aguardando 30 segundos...")
            time.sleep(30)  # 🔹 Verifica a cada 30 segundos

if __name__ == "__main__":
    esperar_ate_horario()
