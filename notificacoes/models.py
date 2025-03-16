from django.db import models
from cloudinary.models import CloudinaryField

class Notificacao(models.Model):
    loja = models.CharField(max_length=255)
    motivo = models.CharField(max_length=255)
    descricao = models.TextField()
    imagem = CloudinaryField('notificacoes', null=True, blank=True)  # 🔹 Agora a imagem será enviada ao Cloudinary
    data_ocorrencia = models.DateField(null=True, blank=True)
    hora_ocorrencia = models.TimeField(verbose_name="Horário")
    notificado_por = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.loja} - {self.motivo}"
