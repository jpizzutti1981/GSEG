from django.db import models

class Notificacao(models.Model):
    loja = models.CharField(max_length=255)
    motivo = models.CharField(max_length=255)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='notificacoes/', null=True, blank=True)
    data_ocorrencia = models.DateField(null=True, blank=True)
    hora_ocorrencia = models.TimeField(verbose_name="Horário")  # 🔹 Certifique-se de que este campo está no modelo!
    notificado_por = models.CharField(max_length=255, null=True, blank=True)
    #itens_notificados = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.loja} - {self.motivo}"
