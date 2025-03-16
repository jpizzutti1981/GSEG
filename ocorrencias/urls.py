from django.urls import path
from django.urls import path
from django.urls import path
from .views import excluir_agendamento, editar_agendamento
from .views import teste_envio_email  # Certifique-se de importar a view corretamente
from django.urls import path, include  # <-- Inclua o 'include' aqui



from .views import (
    listar_ocorrencias,
    cadastrar_ocorrencia,
    editar_ocorrencia,
    excluir_ocorrencia,
    dashboard,
    sinopse,
    gerar_sinopse_pdf,
    configuracao_automacao,
    monitoramento,  
)

urlpatterns = [
    path('', listar_ocorrencias, name='listar_ocorrencias'),
    # Definindo a rota com o nome "automacao"
    path('automacao/', configuracao_automacao, name='automacao'),
    path('cadastrar/', cadastrar_ocorrencia, name='cadastrar_ocorrencia'),
    path('editar/<int:pk>/', editar_ocorrencia, name='editar_ocorrencia'),
    path('excluir/<int:pk>/', excluir_ocorrencia, name='excluir_ocorrencia'),
    path('dashboard/', dashboard, name='dashboard'),
    path('sinopse/', sinopse, name='sinopse'),
    path('sinopse/pdf/<str:data_inicio>/<str:data_fim>/', gerar_sinopse_pdf, name='gerar_sinopse_pdf'),
    path('monitoramento/', monitoramento, name='monitoramento'),
    path('teste-envio-email/', teste_envio_email, name='teste_envio_email'),
    path("excluir_agendamento/<int:agendamento_id>/", excluir_agendamento, name="excluir_agendamento"),
    path("editar_agendamento/<int:agendamento_id>/", editar_agendamento, name="editar_agendamento"),
    path('notificacoes/', include('notificacoes.urls')),
]





