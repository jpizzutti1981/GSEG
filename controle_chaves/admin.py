from django.contrib import admin
from .models import Chave, MovimentacaoChave, ReciclagemVigilante, DocumentoFundamental

admin.site.site_header = "Admin SGSEG"
admin.site.site_title = "Gestão de Segurança"
admin.site.index_title = "Bem-vindo ao Painel Administrativo"

@admin.register(Chave)
class ChaveAdmin(admin.ModelAdmin):
    list_display = ("numero", "nome", "cor_chaveiro", "disponivel")
    list_filter = ("disponivel", "cor_chaveiro")
    search_fields = ("numero", "nome")

@admin.register(MovimentacaoChave)
class MovimentacaoChaveAdmin(admin.ModelAdmin):
    list_display = ("chave", "responsavel", "data_saida", "status")
    list_filter = ("status", "data_saida")
    search_fields = ("responsavel", "telefone")
    ordering = ("-data_saida",)

@admin.register(ReciclagemVigilante)
class ReciclagemVigilanteAdmin(admin.ModelAdmin):
    list_display = ("nome_colaborador", "data_ultima_reciclagem", "vencimento", "status")
    list_filter = ("status",)
    search_fields = ("nome_colaborador",)
    ordering = ("vencimento",)

@admin.register(DocumentoFundamental)
class DocumentoFundamentalAdmin(admin.ModelAdmin):
    list_display = ("nome_documento", "emissao", "vencimento", "status", "area")
    list_filter = ("status", "area")
    search_fields = ("nome_documento", "entidade_emissora")
    ordering = ("vencimento",)

from django.contrib import admin

# 🔹 Define o template customizado SOMENTE após o Django estar carregado
class CustomAdminSite(admin.AdminSite):
    index_template = "admin/base_site.html"

# 🔹 Substitui o admin padrão pelo customizado
admin.site.__class__ = CustomAdminSite

