# Adicionando views de editar e deletar
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import PlanoAcao
from .forms import PlanoAcaoForm
from django.utils.timezone import now
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from .models import PlanoAcao
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import PlanoAcao
from ocorrencias.models import Ocorrencia
from django.db.models import Q
from django.shortcuts import render
from .models import PlanoAcao

@login_required
def listar_planos(request):
    planos = PlanoAcao.objects.all()

    # Coletar filtros da URL
    status = request.GET.get('status', '')
    responsavel = request.GET.get('responsavel', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')

    # Aplicar filtros
    if status:
        planos = planos.filter(status__exact=status)  # Match exato com os valores reais do banco

    if responsavel:
        planos = planos.filter(responsavel__icontains=responsavel)

    if data_inicio and data_fim:
        planos = planos.filter(prazo__range=[data_inicio, data_fim])
    elif data_inicio:
        planos = planos.filter(prazo__gte=data_inicio)
    elif data_fim:
        planos = planos.filter(prazo__lte=data_fim)

    # Lista de opções de status conforme valores no banco
    status_opcoes = [
        ('pendente', 'Pendente'),
        ('em_andamento', 'Em Andamento'),
        ('concluido', 'Concluído'),
    ]

    return render(request, 'planos_acao/listar_planos.html', {
        'planos': planos,
        'status_opcoes': status_opcoes,
        'request_status': status,
        'request_responsavel': responsavel,
        'request_data_inicio': data_inicio,
        'request_data_fim': data_fim,
    })

@login_required
def criar_plano(request):
    if request.method == 'POST':
        form = PlanoAcaoForm(request.POST)
        if form.is_valid():
            plano = form.save(commit=False)
            if request.POST.get('ocorrencia') == 'outro':
                plano.ocorrencia = None  # ✅ Ignora a relação com ocorrência
            plano.save()
            messages.success(request, "✅ Plano salvo com sucesso.")
            return redirect('listar_planos')
        else:
            messages.error(request, "❌ Erro ao salvar o plano. Verifique os dados.")
    else:
        form = PlanoAcaoForm()
    
    return render(request, 'planos_acao/criar_plano.html', {'form': form})

@login_required
def editar_plano(request, plano_id):
    plano = get_object_or_404(PlanoAcao, id=plano_id)

    if request.method == 'POST':
        form = PlanoAcaoForm(request.POST, instance=plano)
        if form.is_valid():
            form.save()
            return redirect('listar_planos')
    else:
        form = PlanoAcaoForm(instance=plano)

    return render(request, 'planos_acao/editar_plano.html', {'form': form, 'plano': plano})

@login_required
def detalhar_plano(request, plano_id):
    plano = get_object_or_404(PlanoAcao, id=plano_id)
    return render(request, 'planos_acao/detalhar_plano.html', {'plano': plano})

@login_required
def deletar_plano(request, plano_id):
    plano = get_object_or_404(PlanoAcao, id=plano_id)

    if request.method == "POST":
        plano.delete()
        messages.success(request, "✅ Plano de ação excluído com sucesso.")
        return redirect('listar_planos')

    return render(request, 'planos_acao/confirmar_exclusao_plano.html', {'plano': plano})
