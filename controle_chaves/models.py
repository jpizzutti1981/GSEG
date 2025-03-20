from datetime import timedelta, date
from django.db import models
from datetime import date
from django.utils import timezone
from cloudinary.models import CloudinaryField
from django.utils import timezone
import os
from cloudinary.models import CloudinaryField
from pdf2image import convert_from_path
import cloudinary.uploader
from django.utils import timezone
import tempfile
import cloudinary
import cloudinary.uploader
from pdf2image import convert_from_path
import requests
from django.db import models


class Chave(models.Model):
    numero = models.CharField(max_length=10, unique=True, verbose_name="Número da Chave")
    nome = models.CharField(max_length=255, default="Chave Desconhecida", verbose_name="Nome da Chave")  
    cor_chaveiro = models.CharField(max_length=50, verbose_name="Cor do Chaveiro")
    disponivel = models.BooleanField(default=True, verbose_name="Disponível")

    def __str__(self):
        return f"{self.numero} - {self.nome} ({self.cor_chaveiro})"

class MovimentacaoChave(models.Model):
    STATUS_CHOICES = [
        ("Devolvida", "Devolvida"),
        ("Não Devolvida", "Não Devolvida"),
    ]

    chave = models.ForeignKey(Chave, on_delete=models.CASCADE, verbose_name="Chave")
    responsavel = models.CharField(max_length=255, verbose_name="Responsável")
    data_saida = models.DateField(auto_now_add=True, verbose_name="Data de Saída")
    horario_saida = models.TimeField(auto_now_add=True, verbose_name="Horário de Saída")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="Não Devolvida", verbose_name="Status")
    operador_saida = models.CharField(max_length=255, verbose_name="Operador de Saída")

    data_devolucao = models.DateField(null=True, blank=True, verbose_name="Data de Devolução")
    horario_devolucao = models.TimeField(null=True, blank=True, verbose_name="Horário de Devolução")
    operador_devolucao = models.CharField(max_length=255, null=True, blank=True, verbose_name="Operador de Devolução")
    
    observacao = models.TextField(blank=True, null=True, verbose_name="Observação")

    def __str__(self):
        return f"Chave {self.chave.numero} - {self.status}"


from cloudinary.models import CloudinaryField

class ReciclagemVigilante(models.Model):
    STATUS_CHOICES = [
        ("No Prazo", "No Prazo"),
        ("Programar Reciclagem", "Programar Reciclagem"),
        ("Vencido", "Vencido"),
    ]

    nome_colaborador = models.CharField(max_length=255, verbose_name="Nome do Colaborador")
    data_ultima_reciclagem = models.DateField(verbose_name="Data da Última Reciclagem")
    vencimento = models.DateField(verbose_name="Data de Vencimento", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name="Status", blank=True)
    dias_para_vencimento = models.IntegerField(verbose_name="Dias para Vencimento", blank=True, null=True)
    diploma = CloudinaryField("diplomas", blank=True, null=True, help_text="Diploma de Reciclagem")

    def calcular_vencimento(self):
        """Define o vencimento com base na data da última reciclagem (+ 720 dias)."""
        return self.data_ultima_reciclagem + timedelta(days=720)

    def calcular_status(self):
        """Atualiza o status com base nos dias para vencimento."""
        hoje = date.today()
        dias_restantes = (self.vencimento - hoje).days

        if dias_restantes > 60:
            return "No Prazo"
        elif 0 < dias_restantes <= 60:
            return "Programar Reciclagem"
        else:
            return "Vencido"

    def save(self, *args, **kwargs):
        """Ao salvar, calcula automaticamente a data de vencimento e status."""
        if not self.vencimento:
            self.vencimento = self.calcular_vencimento()
        self.dias_para_vencimento = (self.vencimento - date.today()).days
        self.status = self.calcular_status()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome_colaborador} - {self.status}"

class DocumentoFundamental(models.Model):
    STATUS_CHOICES = [
        ("No Prazo", "No Prazo"),
        ("Renovar", "Renovar"),
        ("Vencido", "Vencido"),
    ]

    AREA_CHOICES = [
        ("Segurança", "Segurança"),
        ("Administrativo", "Administrativo"),
        ("Estacionamento", "Estacionamento"),
        ("Operacional", "Operacional"),
        ("Outro", "Outro"),
    ]

    nome_documento = models.CharField(max_length=255, verbose_name="Nome do Documento")
    emissao = models.DateField(verbose_name="Data de Emissão")
    vencimento = models.DateField(verbose_name="Data de Vencimento")
    entidade_emissora = models.CharField(max_length=255, verbose_name="Entidade Emissora")
    funcao_documento = models.CharField(max_length=255, verbose_name="Função do Documento")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, verbose_name="Status", blank=True)
    area = models.CharField(max_length=50, choices=AREA_CHOICES, verbose_name="Área")
    arquivo = cloudinary.models.CloudinaryField('documento', blank=True, null=True)
    criado_em = models.DateTimeField(default=timezone.now, verbose_name="Criado em")

    @property
    def validade(self):
        """🔹 Calcula a validade automaticamente"""
        return (self.vencimento - self.emissao).days if self.emissao and self.vencimento else None

    def save(self, *args, **kwargs):
        """🔹 Atualiza status automaticamente e converte PDF para imagem se necessário"""
        
        # 🔹 Calcula o status automaticamente antes de salvar
        dias_restantes = (self.vencimento - timezone.now().date()).days
        if dias_restantes > 60:
            self.status = "No Prazo"
        elif 0 <= dias_restantes <= 60:
            self.status = "Renovar"
        else:
            self.status = "Vencido"

        # 🔹 Salva o documento no Cloudinary antes de converter PDF
        super().save(*args, **kwargs)

        # 🔹 Se o arquivo for um PDF, converte para imagem
        if self.arquivo and str(self.arquivo).endswith('.pdf'):
            imagem_url = self.convert_pdf_to_image(self.arquivo.url)
            if imagem_url:
                self.arquivo = imagem_url
                super().save(update_fields=["arquivo"])  # Atualiza apenas o arquivo convertido

    def convert_pdf_to_image(self, pdf_url):
        """🔹 Faz download do PDF, converte para imagem e faz upload para Cloudinary"""

        try:
            # 🔹 Faz download do PDF
            response = requests.get(pdf_url, stream=True)
            response.raise_for_status()

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                for chunk in response.iter_content(chunk_size=8192):
                    temp_pdf.write(chunk)
                temp_pdf_path = temp_pdf.name

            # 🔹 Converte PDF em imagem
            poppler_path = os.path.join(os.path.dirname(__file__), '..', 'poppler', 'Library', 'bin')
            images = convert_from_path(temp_pdf_path, poppler_path=poppler_path)
            if images:
                temp_img_path = temp_pdf_path.replace(".pdf", ".jpg")
                images[0].save(temp_img_path, "JPEG")

                # 🔹 Faz upload para Cloudinary
                upload_result = cloudinary.uploader.upload(temp_img_path)

                # 🔹 Remove arquivos temporários
                os.remove(temp_pdf_path)
                os.remove(temp_img_path)

                return upload_result["secure_url"]

        except Exception as e:
            print(f"Erro na conversão do PDF para imagem: {e}")

        return None
    
class AtendimentoAmbulatorial(models.Model):
    data = models.DateField(verbose_name="Data")
    mes = models.CharField(max_length=20, verbose_name="Mês")
    trimestre = models.IntegerField(verbose_name="Trimestre")
    ano = models.IntegerField(verbose_name="Ano")
    
    qtde_atendimentos = models.IntegerField(verbose_name="Qtde Atendimentos", default=0)
    qtde_chamados = models.IntegerField(verbose_name="Qtde Chamados", default=0)
    qtde_remocoes = models.IntegerField(verbose_name="Qtde Remoções", default=0)
    resolvidos = models.IntegerField(verbose_name="Resolvidos", default=0)

    qtde_clientes = models.IntegerField(verbose_name="Qtde Clientes", default=0)
    qtde_lojistas = models.IntegerField(verbose_name="Qtde Lojistas", default=0)
    qtde_homens = models.IntegerField(verbose_name="Qtde Homens", default=0)
    qtde_mulheres = models.IntegerField(verbose_name="Qtde Mulheres", default=0)

    ambulatorial = models.IntegerField(verbose_name="Ambulatorial", default=0)
    traumatologico = models.IntegerField(verbose_name="Traumatológico", default=0)

    colaboradores_terceiros = models.IntegerField(verbose_name="Colaboradores Terceiros", default=0)
    colaboradores_organicos = models.IntegerField(verbose_name="Colaboradores Orgânicos", default=0)
    prestadores_servico = models.IntegerField(verbose_name="Prestadores de Serviço", default=0)

    def __str__(self):
        return f"{self.data} - {self.qtde_atendimentos} Atendimentos"

class Colaborador(models.Model):
    TIPOS_USUARIO = [
        ("Vigilante", "Vigilante"),
        ("Funcionário", "Funcionário"),
        ("Prestador", "Prestador de Serviço"),
        ("Lojista", "Lojista"),
        ("Administração", "Administração"),
        ("Comercial", "Comercial"),
        ("Segurança", "Segurança"),
        ("Estacionamento", "Estacionamento"),
        ("Manutenção", "Manutenção"),
    ]
    
    nome_completo = models.CharField(max_length=255, verbose_name="Nome Completo")
    telefone = models.CharField(max_length=20, verbose_name="Telefone")
    email = models.EmailField(unique=True, verbose_name="E-mail")
    funcao = models.CharField(max_length=100, verbose_name="Função")
    tipo = models.CharField(max_length=20, choices=TIPOS_USUARIO, verbose_name="Tipo de Usuário")

    def __str__(self):
        return self.nome_completo