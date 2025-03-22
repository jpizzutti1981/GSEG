from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_planos, name='listar_planos'),
    path('criar/', views.criar_plano, name='criar_plano'),
    path('editar/<int:plano_id>/', views.editar_plano, name='editar_plano'),
    path('detalhar/<int:plano_id>/', views.detalhar_plano, name='detalhar_plano'),
    path('deletar/<int:plano_id>/', views.deletar_plano, name='deletar_plano'),
]