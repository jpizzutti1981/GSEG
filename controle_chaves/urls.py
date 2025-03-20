from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    # 🔑 Controle de Chaves
    path("chaves/", views.listar_chaves, name="listar_chaves"),
    path("movimentacoes/", views.listar_movimentacoes, name="listar_movimentacoes"),
    path("registrar-saida/", views.registrar_saida, name="registrar_saida"),
    path("devolucao/<int:movimentacao_id>/", views.registrar_devolucao, name="registrar_devolucao"),
    path("cadastrar/", views.cadastrar_chave, name="cadastrar_chave"),
    path("editar/<int:chave_id>/", views.editar_chave, name="editar_chave"),
    path("deletar/<int:chave_id>/", views.deletar_chave, name="deletar_chave"),
    path("editar-saida/<int:movimentacao_id>/", views.editar_saida, name="editar_saida"),

    # ♻️ Reciclagens
    path("reciclagens/", views.listar_reciclagens, name="listar_reciclagens"),
    path("reciclagens/adicionar/", views.adicionar_reciclagem, name="adicionar_reciclagem"),
    path("reciclagens/editar/<int:reciclagem_id>/", views.editar_reciclagem, name="editar_reciclagem"),
    path("reciclagens/excluir/<int:reciclagem_id>/", views.excluir_reciclagem, name="excluir_reciclagem"),

    # 📄 Documentos
    path("documentos/", views.listar_documentos, name="listar_documentos"),
    path("documentos/adicionar/", views.adicionar_documento, name="adicionar_documento"),
    path("documentos/editar/<int:documento_id>/", views.editar_documento, name="editar_documento"),
    path("documentos/excluir/<int:documento_id>/", views.excluir_documento, name="excluir_documento"),

    # 👥 Atendimento e Dashboard
    path("atendimentos/", views.listar_atendimentos, name="listar_atendimentos"),
    path("atendimentos/adicionar/", views.adicionar_atendimento, name="adicionar_atendimento"),
    path("atendimentos/editar/<int:atendimento_id>/", views.editar_atendimento, name="editar_atendimento"),
    path("atendimentos/excluir/<int:atendimento_id>/", views.excluir_atendimento, name="excluir_atendimento"),
    path("atendimentos/dashboard/", views.dashboard_atendimentos, name="dashboard_atendimentos"),

    # 👤 Gestão de Usuários (Colaboradores)
    path("colaboradores/cadastrar/", views.cadastrar_colaborador, name="cadastrar_colaborador"),
    path("usuarios/", views.listar_usuarios, name="listar_usuarios"),
    path("usuarios/editar/<int:usuario_id>/", views.editar_usuario, name="editar_usuario"),
    path("usuarios/deletar/<int:usuario_id>/", views.deletar_usuario, name="deletar_usuario"),
    path("buscar-dados-colaborador/", views.buscar_dados_colaborador, name="buscar_dados_colaborador"),  # ✅ Adicionado para AJAX

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.index_template = "admin/base_site.html"
