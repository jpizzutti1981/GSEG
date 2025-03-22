from django.db import models
from ocorrencias.models import Ocorrencia

class PlanoAcao(models.Model):
    ocorrencia = models.ForeignKey(Ocorrencia, on_delete=models.SET_NULL, null=True, blank=True)
    descricao = models.TextField()
    responsavel = models.CharField(max_length=255)
    prazo = models.DateField()
    status = models.CharField(max_length=50, choices=[
        ('Pendente', 'Pendente'),
        ('Em andamento', 'Em andamento'),
        ('Concluído', 'Concluído')
    ])

    def __str__(self):
        return self.descricao