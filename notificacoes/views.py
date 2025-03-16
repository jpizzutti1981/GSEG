from django.shortcuts import render, redirect
from .forms import NotificacaoForm
from .utils import enviar_mensagem_telegram, gerar_pdf_notificacao
from django.shortcuts import render
from .models import Notificacao
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Notificacao
from .forms import NotificacaoForm
from django.contrib import messages
from django.http import FileResponse, Http404
from django.http import HttpResponse
from django.conf import settings
import os
from django.shortcuts import render, get_object_or_404
from .models import Notificacao
from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.http import Http404
from .forms import NotificacaoForm
from .models import Notificacao
from .utils import enviar_mensagem_telegram, gerar_pdf_notificacao
from django.db.models import Q
from django.shortcuts import render
from .models import Notificacao

from django.shortcuts import render
from django.db.models import Q
from .models import Notificacao
from datetime import datetime
from django.utils import timezone

@login_required
def criar_notificacao(request):
    if request.method == 'POST':
        form = NotificacaoForm(request.POST, request.FILES)
        if form.is_valid():
            notificacao = form.save(commit=False)  # 🔹 Ainda não salva no banco

            # 🔹 Garante que a data e hora da ocorrência sejam preenchidas corretamente
            notificacao.data_ocorrencia = notificacao.data_ocorrencia or now().date()
            notificacao.hora_ocorrencia = notificacao.hora_ocorrencia or now().time()

            notificacao.save()  # 🔹 Agora salva com os valores atualizados

            # 🔹 Gera o PDF e obtém o caminho
            try:
                pdf_path = gerar_pdf_notificacao(notificacao) 
                if not pdf_path:
                    messages.error(request, "⚠️ Erro ao gerar o PDF da notificação.")
            except Exception as e:
                messages.error(request, f"⚠️ Erro ao gerar PDF: {str(e)}")
                pdf_path = None  # 🔹 Evita que a aplicação quebre

            # 🔹 Envia mensagem para o Telegram com os detalhes da notificação
            mensagem = (
                f"📝 <b>Nova Notificação</b>\n"
                f"🏬 Loja: {notificacao.loja}\n"
                f"✍ Motivo: {notificacao.motivo}\n"
                f"📅 Data: {notificacao.data_ocorrencia.strftime('%d/%m/%Y')} às {notificacao.hora_ocorrencia.strftime('%H:%M')}"
            )
            enviar_mensagem_telegram(mensagem=mensagem)

            # ✅ Mensagem de sucesso antes do redirecionamento
            messages.success(request, "✅ Notificação cadastrada com sucesso!")

            return redirect('criar_notificacao')  # 🔹 Mantém na mesma página para exibir mensagem
    else:
        form = NotificacaoForm()

    return render(request, 'notificacoes/notificacao_form.html', {'form': form})

@login_required
def listar_notificacoes(request):
    loja = request.GET.get("loja", "").strip()
    data = request.GET.get("data", "").strip()
    motivo = request.GET.get("motivo", "").strip()

    notificacoes = Notificacao.objects.all()

    print(f"🔎 FILTROS RECEBIDOS - Loja: {loja}, Data: {data}, Motivo: {motivo}")

    # 🔹 Filtra por loja
    if loja:
        notificacoes = notificacoes.filter(loja__icontains=loja)

    # 🔹 Filtra por data (corrigido para o formato correto do banco)
    if data:
        try:
            data_formatada = datetime.strptime(data, "%Y-%m-%d").date()
            notificacoes = notificacoes.filter(data_ocorrencia=data_formatada)
        except ValueError:
            print("⚠ ERRO: Data inválida informada.")

    # 🔹 Filtra por motivo (corrigido para funcionar corretamente)
    if motivo:
        notificacoes = notificacoes.filter(motivo__icontains=motivo)

    print(f"🔎 RESULTADO FINAL: {notificacoes.count()} notificações encontradas.")

    return render(request, "notificacoes/listar_notificacoes.html", {
        "notificacoes": notificacoes,
        "loja": loja,
        "data": data,
        "motivo": motivo
    })

@login_required
def editar_notificacao(request, pk):
    notificacao = get_object_or_404(Notificacao, pk=pk)
    
    if request.method == 'POST':
        form = NotificacaoForm(request.POST, request.FILES, instance=notificacao)
        if form.is_valid():
            form.save()
            messages.success(request, "Notificação atualizada com sucesso!")
            return redirect('listar_notificacoes')
    else:
        form = NotificacaoForm(instance=notificacao)

    return render(request, 'notificacoes/editar_notificacao.html', {'form': form, 'notificacao': notificacao})

@login_required
def excluir_notificacao(request, pk):
    notificacao = get_object_or_404(Notificacao, pk=pk)
    
    if request.method == 'POST':
        notificacao.delete()
        messages.success(request, "Notificação excluída com sucesso!")
        return redirect('listar_notificacoes')

    return render(request, 'notificacoes/confirmar_exclusao.html', {'notificacao': notificacao})

@login_required
def download_pdf(request, pk):
    """ Baixa o PDF da notificação """
    try:
        notificacao = Notificacao.objects.get(pk=pk)
    except Notificacao.DoesNotExist:
        raise Http404("Notificação não encontrada.")

    # 🔹 Gera o PDF se não existir
    pdf_path = gerar_pdf_notificacao(notificacao)

    if os.path.exists(pdf_path):
        return FileResponse(open(pdf_path, 'rb'), content_type='application/pdf', as_attachment=True)
    else:
        raise Http404("Arquivo PDF não encontrado.")
    
@login_required
def detalhar_notificacao(request, pk):
    notificacao = get_object_or_404(Notificacao, pk=pk)

    # 🔹 Processa os itens antes de enviar para o template
    #itens_notificados = []
    #if notificacao.itens_notificados and notificacao.itens_notificados != "Nenhum item registrado":
        #itens_notificados = [item.strip() for item in notificacao.itens_notificados.split(",")]

    return render(request, "notificacoes/detalhar_notificacao.html", {
        "notificacao": notificacao,
        #"itens_notificados": itens_notificados  # 🔹 Agora o template recebe uma lista correta
    })
