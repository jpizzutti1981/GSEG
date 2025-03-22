import logging
from core.models import LogEntry

logger = logging.getLogger("custom")

def registrar_log(nivel, mensagem):
    """Salva logs no banco e também no console/arquivo"""
    LogEntry.objects.create(nivel=nivel, mensagem=mensagem)

    nivel_log = getattr(logging, nivel.upper(), logging.INFO)
    logger.log(nivel_log, mensagem)
