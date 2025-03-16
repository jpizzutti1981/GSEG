from django.urls import path
from .views import criar_notificacao  # confirme o nome exato desta view
from .views import listar_notificacoes
from .views import editar_notificacao
from .views import excluir_notificacao
from .views import download_pdf
from .views import detalhar_notificacao
from .views import download_pdf

urlpatterns = [
    path('criar/', criar_notificacao, name='criar_notificacao'),
    path('listar/', listar_notificacoes, name='listar_notificacoes'),
    path('editar/<int:pk>/', editar_notificacao, name='editar_notificacao'),
    path('excluir/<int:pk>/', excluir_notificacao, name='excluir_notificacao'),
    path('download/<int:notificacao_id>/', download_pdf, name='download_pdf'),
    path('<int:pk>/', detalhar_notificacao, name='detalhar_notificacao'), 
    path('<int:pk>/pdf/', download_pdf, name='baixar_pdf_notificacao'), 
    path('<int:notificacao_id>/pdf/', download_pdf, name='baixar_pdf_notificacao'),
]
