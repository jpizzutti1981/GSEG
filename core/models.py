from django.db import models

class LogEntry(models.Model):
    """📌 Modelo para armazenar logs no banco de dados."""
    nivel = models.CharField(max_length=50)
    mensagem = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.nivel}] {self.mensagem[:60]}..."
