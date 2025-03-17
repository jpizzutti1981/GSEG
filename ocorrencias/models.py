from django.db import models
from django.utils.timezone import now
from datetime import datetime
from cloudinary.models import CloudinaryField

class TipoOcorrencia(models.Model):
    nome = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nome

class Local(models.Model):
    nome = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nome

class Ocorrencia(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em_andamento', 'Em andamento'),
        ('concluido', 'Concluído'),
    ]

    data_ocorrencia = models.DateField()
    horario = models.TimeField(verbose_name="Horário")
    tipo = models.ForeignKey(TipoOcorrencia, on_delete=models.CASCADE)
    local = models.ForeignKey(Local, on_delete=models.CASCADE)
    nome_local = models.CharField(max_length=100)
    relato = models.TextField()
    imagem = CloudinaryField('ocorrencias', null=True, blank=True) 
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pendente')
    responsavel = models.CharField(max_length=100)
    envolvidos = models.TextField(blank=True, null=True)
    acoes_tomadas = models.TextField(blank=True, null=True)
    supervisor = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        """Força a conversão do horário para garantir o formato correto"""
        if isinstance(self.horario, str):
            try:
                self.horario = datetime.strptime(self.horario, "%H:%M").time()
            except ValueError:
                self.horario = now().time()  # Se falhar, salva com o horário atual

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tipo} - {self.local} ({self.status})"

class ConfiguracaoAutomacao(models.Model):
    emails_destinatarios = models.TextField(blank=True, null=True)
    horario_envio = models.TimeField(default="12:00") 
    assunto = models.CharField(max_length=255, default="Sinopse Diária - ")
    mensagem = models.TextField(default="Segue, anexo, sinopse diária.")
    horario_envio = models.TimeField(help_text="Horário do envio diário")
    
    def __str__(self):
        return f"Configuração de Automação - {self.horario_envio}"

class LogSinopse(models.Model):
    data_execucao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255)
    detalhes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.data_execucao} - {self.status}"

class Agendamento(models.Model):
    emails_destinatarios = models.TextField(help_text="E-mails separados por vírgula")
    horario_envio = models.TimeField()
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"Agendamento às {self.horario_envio} - {self.emails_destinatarios}"


