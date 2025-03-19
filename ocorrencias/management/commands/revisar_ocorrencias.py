import os
import openai
import time
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from ocorrencias.models import Ocorrencia
from dotenv import load_dotenv

# 🔹 Carregar variáveis do .env
load_dotenv()

# 🔹 Obter a API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("⚠️ ERRO: OPENAI_API_KEY não foi definida. Verifique o arquivo .env.")

# 🔹 Inicializar o cliente OpenAI corretamente
client = openai.OpenAI(api_key=OPENAI_API_KEY)

class Command(BaseCommand):
    help = "Revisa os relatos e ações tomadas das ocorrências do dia anterior usando IA"

    def handle(self, *args, **kwargs):
        print("🚀 Worker de Revisão de Ocorrências iniciado! Aguardando horário correto...")

        while True:
            horario_atual = datetime.now().strftime("%H:%M")
            horario_programado = "01:00"  # 🔹 Garante que será executado às 01h todos os dias

            print(f"🔍 [DEBUG] Agora: {horario_atual} | Horário programado: {horario_programado}")

            if horario_atual == horario_programado:
                print("🕒 01:00 - Iniciando revisão de ocorrências...")

                ontem = datetime.now() - timedelta(days=1)
                data_ontem = ontem.strftime("%Y-%m-%d")

                # 🔹 Filtrar ocorrências do dia anterior
                ocorrencias = Ocorrencia.objects.filter(data_ocorrencia=data_ontem)

                if not ocorrencias.exists():
                    print("⚠️ Nenhuma ocorrência para revisar.")
                else:
                    for ocorrencia in ocorrencias:
                        print(f"✍️ Revisando ocorrência ID {ocorrencia.id}...")

                        relato_corrigido = self.revisar_texto(ocorrencia.relato)
                        acoes_corrigidas = self.revisar_texto(ocorrencia.acoes_tomadas)

                        # 🔹 Atualizar ocorrências
                        ocorrencia.relato = relato_corrigido
                        ocorrencia.acoes_tomadas = acoes_corrigidas
                        ocorrencia.save()

                    print(f"✅ {ocorrencias.count()} ocorrências revisadas com sucesso!")

                print("⏳ Aguardando 24h para a próxima execução...")
                time.sleep(86400)  # 🔹 Aguarda 24h para a próxima execução

            else:
                print("⏳ Ainda não é a hora, aguardando 30 segundos...")
                time.sleep(30)  # 🔹 Verifica a cada 30 segundos

    def revisar_texto(self, texto):
        """🔹 Função para revisar e corrigir um texto usando OpenAI."""
        if not texto:
            return texto  # Evita erro se o campo estiver vazio

        prompt = (
            "Revise o seguinte texto e corrija erros gramaticais, ortográficos e melhore a clareza. "
            "Mantenha o sentido original e a formalidade do texto. Responda apenas com o texto revisado, "
            "sem introduções ou explicações adicionais.\n\n"
            f"Texto original:\n{texto}"
        )

        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.strip()

        except Exception as e:
            return f"Erro na revisão: {str(e)}"