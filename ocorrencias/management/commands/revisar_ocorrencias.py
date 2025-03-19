import os
import openai
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

class Command(BaseCommand):  # 🔹 Corrigir nome da classe para "Command"
    help = "Revisa os relatos e ações tomadas das ocorrências do dia anterior usando IA"

    def handle(self, *args, **kwargs):
        self.stdout.write("🚀 Iniciando revisão de ocorrências...")

        ontem = datetime.now() - timedelta(days=1)
        data_ontem = ontem.strftime("%Y-%m-%d")

        # 🔹 Filtrar ocorrências do dia anterior
        ocorrencias = Ocorrencia.objects.filter(data_ocorrencia=data_ontem)

        if not ocorrencias.exists():
            self.stdout.write(self.style.WARNING("⚠ Nenhuma ocorrência para revisar."))
            return

        for ocorrencia in ocorrencias:
            relato_corrigido = self.revisar_texto(ocorrencia.relato)
            acoes_corrigidas = self.revisar_texto(ocorrencia.acoes_tomadas)

            # 🔹 Atualizar ocorrências
            ocorrencia.relato = relato_corrigido
            ocorrencia.acoes_tomadas = acoes_corrigidas
            ocorrencia.save()

        self.stdout.write(self.style.SUCCESS(f"✅ {ocorrencias.count()} ocorrências revisadas com sucesso!"))

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
            return f"❌ Erro na revisão: {str(e)}"
