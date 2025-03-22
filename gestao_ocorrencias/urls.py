from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import login_view, logout_view  # Importa também a logout_view
from django.urls import path, include

# Função para redirecionar após login
def custom_login_redirect(request):
    return redirect('listar_ocorrencias')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ocorrencias.urls')),
    # Rota para /login/ utilizando a view do app accounts
    path('login/', login_view, name='login'),
    # Rota para logout, utilizando a logout_view importada
    path('logout/', logout_view, name='logout'),
    path('accounts/profile/', custom_login_redirect),
    path('accounts/', include('accounts.urls')),
    path("controle_chaves/", include("controle_chaves.urls")),
    path("planos/", include("planos_acao.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
