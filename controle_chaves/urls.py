from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("chaves/", views.listar_chaves, name="listar_chaves"),
    path("movimentacoes/", views.listar_movimentacoes, name="listar_movimentacoes"),
    path("registrar-saida/", views.registrar_saida, name="registrar_saida"),
    path("devolucao/<int:movimentacao_id>/", views.registrar_devolucao, name="registrar_devolucao"),
    path("cadastrar/", views.cadastrar_chave, name="cadastrar_chave"),
    path("editar/<int:chave_id>/", views.editar_chave, name="editar_chave"),  # ✅ Editar Chave
    path("deletar/<int:chave_id>/", views.deletar_chave, name="deletar_chave"),  # ✅ Deletar Chave
    path("editar-saida/<int:movimentacao_id>/", views.editar_saida, name="editar_saida"),  # ✅ Nova rota para editar saída
    path("reciclagens/", views.listar_reciclagens, name="listar_reciclagens"),
    path("reciclagens/adicionar/", views.adicionar_reciclagem, name="adicionar_reciclagem"),
    path("reciclagens/editar/<int:reciclagem_id>/", views.editar_reciclagem, name="editar_reciclagem"),
    path("reciclagens/excluir/<int:reciclagem_id>/", views.excluir_reciclagem, name="excluir_reciclagem"),
    path("documentos/", views.listar_documentos, name="listar_documentos"),
    path("documentos/adicionar/", views.adicionar_documento, name="adicionar_documento"),
    path("documentos/editar/<int:documento_id>/", views.editar_documento, name="editar_documento"),
    path("documentos/excluir/<int:documento_id>/", views.excluir_documento, name="excluir_documento"),
    path("atendimentos/", views.listar_atendimentos, name="listar_atendimentos"),
    path("atendimentos/adicionar/", views.adicionar_atendimento, name="adicionar_atendimento"),
    path("atendimentos/editar/<int:atendimento_id>/", views.editar_atendimento, name="editar_atendimento"),
    path("atendimentos/excluir/<int:atendimento_id>/", views.excluir_atendimento, name="excluir_atendimento"),
    path("atendimentos/dashboard/", views.dashboard_atendimentos, name="dashboard_atendimentos"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.contrib import admin
admin.site.index_template = "admin/base_site.html"

