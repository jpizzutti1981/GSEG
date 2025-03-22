import logging
from django.apps import apps

class DatabaseLogHandler(logging.Handler):
    """🔥 Captura logs e salva no banco de dados automaticamente."""

    def emit(self, record):
        try:
            LogEntry = apps.get_model("core", "LogEntry")  # 🔹 Obtém o modelo dinamicamente
            nivel = record.levelname
            mensagem = self.format(record)

            LogEntry.objects.create(nivel=nivel, mensagem=mensagem)
        except Exception as e:
            print(f"⚠️ Erro ao salvar log no banco: {e}")  # Evita crash total caso ocorra erro
