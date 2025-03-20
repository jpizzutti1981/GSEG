from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Chave, MovimentacaoChave
from .forms import MovimentacaoChaveForm, ChaveForm
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import MovimentacaoChave
from .forms import MovimentacaoChaveForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import ReciclagemVigilante
from .forms import ReciclagemVigilanteForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import DocumentoFundamental
from .forms import DocumentoFundamentalForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import AtendimentoAmbulatorial
from .forms import AtendimentoAmbulatorialForm
from django.shortcuts import render
from django.db.models import Q
from .models import AtendimentoAmbulatorial
from django.shortcuts import render
from django.db.models import Sum, Count
from .models import AtendimentoAmbulatorial
import json
from django.shortcuts import render
from django.db.models import Sum
from .models import AtendimentoAmbulatorial
from django.db.models import Sum
from django.shortcuts import render, redirect
from .models import Colaborador
from .forms import ColaboradorForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Colaborador
from .forms import ColaboradorForm  # Criamos esse formulário no próximo passo
from django.contrib import messages

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Colaborador

# ✅ LISTAR CHAVES (MOSTRA AS CHAVES DISPONÍVEIS)
@login_required
def listar_chaves(request):
    """Lista todas as chaves com filtro de pesquisa por número, nome e disponibilidade."""

    # 🔹 Obtém os parâmetros de pesquisa do formulário (GET)
    numero_filtro = request.GET.get("numero", "").strip()
    nome_filtro = request.GET.get("nome", "").strip()
    disponivel_filtro = request.GET.get("disponivel", "")

    # 🔹 Filtra as chaves com base nos critérios informados
    chaves = Chave.objects.all()

    if numero_filtro:
        chaves = chaves.filter(numero__icontains=numero_filtro)

    if nome_filtro:
        chaves = chaves.filter(nome__icontains=nome_filtro)

    if disponivel_filtro:
        if disponivel_filtro.lower() == "sim":
            chaves = chaves.filter(disponivel=True)
        elif disponivel_filtro.lower() == "nao":
            chaves = chaves.filter(disponivel=False)

    # 🔹 Ordenação numérica correta (mantém números em ordem)
    chaves_ordenadas = sorted(
        chaves,
        key=lambda chave: int(''.join(filter(str.isdigit, chave.numero))) if chave.numero.isdigit() else float('inf')
    )

    return render(
        request,
        "controle_chaves/listar_chaves.html",
        {"chaves": chaves_ordenadas, "numero_filtro": numero_filtro, "nome_filtro": nome_filtro, "disponivel_filtro": disponivel_filtro}
    )

# ✅ LISTAR MOVIMENTAÇÕES COM FILTRO
@login_required
def listar_movimentacoes(request):
    """Lista todas as movimentações de chaves registradas, com filtro de status."""
    filtro_status = request.GET.get('status', '')  # Pega o valor do filtro na URL
    movimentacoes = MovimentacaoChave.objects.all().order_by('-data_saida')

    # Se um filtro foi aplicado, filtra os resultados
    if filtro_status in ['Devolvida', 'Não Devolvida']:
        movimentacoes = movimentacoes.filter(status=filtro_status)

    return render(request, "controle_chaves/listar_movimentacoes.html", {
        "movimentacoes": movimentacoes,
        "filtro_status": filtro_status
    })

# ✅ REGISTRAR SAÍDA (IMPEDINDO CHAVES JÁ EMPRESTADAS)
@login_required
def registrar_saida(request):
    """Registra a saída de uma chave e impede saídas duplicadas."""

    colaboradores = Colaborador.objects.all()  # 🔹 Carregar lista de colaboradores
    chaves_disponiveis = Chave.objects.filter(disponivel=True)

    if request.method == "POST":
        form = MovimentacaoChaveForm(request.POST)
        if form.is_valid():
            movimentacao = form.save(commit=False)

            # Verifica se a chave já está emprestada
            if not movimentacao.chave.disponivel:
                messages.error(request, "❌ Essa chave já está emprestada!")
                return redirect("registrar_saida")

            movimentacao.status = "Não Devolvida"
            movimentacao.save()

            # Atualiza o status da chave para "Indisponível"
            movimentacao.chave.disponivel = False
            movimentacao.chave.save()

            messages.success(request, "✅ Saída da chave registrada com sucesso!")
            return redirect("registrar_saida")

        else:
            messages.error(request, "❌ Erro ao registrar saída. Verifique os dados.")

    form = MovimentacaoChaveForm()

    return render(request, "controle_chaves/registrar_saida.html", {
        "form": form,
        "chaves_disponiveis": chaves_disponiveis,
        "colaboradores": colaboradores
    })

# ✅ REGISTRAR DEVOLUÇÃO DE CHAVE
@login_required
def registrar_devolucao(request, movimentacao_id):
    """Registra a devolução de uma chave e atualiza o status."""
    movimentacao = get_object_or_404(MovimentacaoChave, id=movimentacao_id)
    
    if request.method == "POST":
        movimentacao.data_devolucao = datetime.now().date()
        movimentacao.horario_devolucao = datetime.now().time()
        movimentacao.status = "Devolvida"
        movimentacao.save()

        # Atualiza o status da chave para disponível
        chave = movimentacao.chave
        chave.disponivel = True
        chave.save()

        messages.success(request, "✅ Chave devolvida com sucesso!")
        return redirect("listar_movimentacoes")

    return render(request, "controle_chaves/registrar_devolucao.html", {"movimentacao": movimentacao})

# ✅ CADASTRAR NOVA CHAVE
@login_required
def cadastrar_chave(request):
    """Cadastra uma nova chave no sistema."""
    if request.method == "POST":
        form = ChaveForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Chave cadastrada com sucesso!")
            return redirect("listar_chaves")
        else:
            messages.error(request, "❌ Erro ao cadastrar chave.")

    form = ChaveForm()
    return render(request, "controle_chaves/cadastrar_chave.html", {"form": form})

@login_required
def editar_chave(request, chave_id):
    """Edita o cadastro de uma chave."""
    chave = get_object_or_404(Chave, id=chave_id)

    if request.method == "POST":
        form = ChaveForm(request.POST, instance=chave)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Chave atualizada com sucesso!")
            return redirect("listar_chaves")
        else:
            messages.error(request, "❌ Erro ao atualizar a chave. Verifique os dados.")
    
    form = ChaveForm(instance=chave)
    return render(request, "controle_chaves/editar_chave.html", {"form": form, "chave": chave})

@login_required
def deletar_chave(request, chave_id):
    """Deleta uma chave do sistema."""
    chave = get_object_or_404(Chave, id=chave_id)

    if request.method == "POST":
        chave.delete()
        messages.success(request, "✅ Chave deletada com sucesso!")
        return redirect("listar_chaves")

    return render(request, "controle_chaves/deletar_chave.html", {"chave": chave})

@login_required
def editar_saida(request, movimentacao_id):
    movimentacao = get_object_or_404(MovimentacaoChave, id=movimentacao_id)

    if request.method == "POST":
        form = MovimentacaoChaveForm(request.POST, instance=movimentacao)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Registro de saída atualizado com sucesso!")
            return redirect("listar_movimentacoes")
    else:
        form = MovimentacaoChaveForm(instance=movimentacao)

    return render(request, "controle_chaves/editar_saida.html", {"form": form})

def listar_reciclagens(request):
    reciclagens = ReciclagemVigilante.objects.all().order_by("vencimento")
    return render(request, "reciclagem/listar_reciclagens.html", {"reciclagens": reciclagens})

def adicionar_reciclagem(request):
    if request.method == "POST":
        form = ReciclagemVigilanteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Reciclagem cadastrada com sucesso!")
            return redirect("listar_reciclagens")
    
    form = ReciclagemVigilanteForm()
    return render(request, "reciclagem/adicionar_reciclagem.html", {"form": form})

def editar_reciclagem(request, reciclagem_id):
    reciclagem = get_object_or_404(ReciclagemVigilante, id=reciclagem_id)

    if request.method == "POST":
        form = ReciclagemVigilanteForm(request.POST, request.FILES, instance=reciclagem)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Reciclagem atualizada com sucesso!")
            return redirect("listar_reciclagens")

    form = ReciclagemVigilanteForm(instance=reciclagem)
    return render(request, "reciclagem/editar_reciclagem.html", {"form": form, "reciclagem": reciclagem})

def excluir_reciclagem(request, reciclagem_id):
    reciclagem = get_object_or_404(ReciclagemVigilante, id=reciclagem_id)
    reciclagem.delete()
    messages.success(request, "✅ Reciclagem excluída com sucesso!")
    return redirect("listar_reciclagens")

def listar_documentos(request):
    documentos = DocumentoFundamental.objects.all().order_by("vencimento")
    return render(request, "documentos/listar_documentos.html", {"documentos": documentos})

def adicionar_documento(request):
    if request.method == "POST":
        form = DocumentoFundamentalForm(request.POST, request.FILES)  # 🔹 Agora aceita arquivos
        if form.is_valid():
            form.save()
            messages.success(request, "Documento adicionado com sucesso! 📄")
            return redirect("listar_documentos")
        else:
            messages.error(request, "Erro ao salvar documento. Verifique os campos.")
    else:
        form = DocumentoFundamentalForm()

    return render(request, "documentos/adicionar_documento.html", {"form": form})

def editar_documento(request, documento_id):
    documento = get_object_or_404(DocumentoFundamental, id=documento_id)
    
    if request.method == "POST":
        form = DocumentoFundamentalForm(request.POST, request.FILES, instance=documento)
        if form.is_valid():
            form.save()
            messages.success(request, "📄 Documento atualizado com sucesso!")
            return redirect("listar_documentos")
        else:
            messages.error(request, "❌ Erro ao atualizar o documento. Verifique os campos.")
    else:
        form = DocumentoFundamentalForm(instance=documento)

    return render(request, "documentos/editar_documento.html", {"form": form, "documento": documento})

def excluir_documento(request, documento_id):
    documento = get_object_or_404(DocumentoFundamental, id=documento_id)
    documento.delete()
    messages.success(request, "✅ Documento excluído com sucesso!")
    return redirect("listar_documentos")

# 🔹 Listar Atendimentos
def listar_atendimentos(request):
    modo_exibicao = request.GET.get('modo', 'tabela')  # Define o modo de exibição

    atendimentos = AtendimentoAmbulatorial.objects.all().order_by("-data")

    # Cálculo dos acumulados do ano
    acumulados = atendimentos.aggregate(
        total_atendimentos=Sum('qtde_atendimentos'),
        total_remocoes=Sum('qtde_remocoes'),
        total_clientes=Sum('qtde_clientes'),
        total_lojistas=Sum('qtde_lojistas'),
        total_homens=Sum('qtde_homens'),
        total_mulheres=Sum('qtde_mulheres')
    )

    context = {
        "atendimentos": atendimentos,
        "modo_exibicao": modo_exibicao,
        "acumulados": acumulados,  # Passa os acumulados para o template
    }

    return render(request, "atendimentos/listar.html", context)

# 🔹 Adicionar Atendimento
def adicionar_atendimento(request):
    if request.method == "POST":
        form = AtendimentoAmbulatorialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Atendimento registrado com sucesso!")
            return redirect("listar_atendimentos")
    else:
        form = AtendimentoAmbulatorialForm()

    return render(request, "atendimentos/adicionar.html", {"form": form})

# 🔹 Editar Atendimento
def editar_atendimento(request, atendimento_id):
    atendimento = get_object_or_404(AtendimentoAmbulatorial, id=atendimento_id)

    if request.method == "POST":
        form = AtendimentoAmbulatorialForm(request.POST, instance=atendimento)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Atendimento atualizado com sucesso!")
            return redirect("listar_atendimentos")
    else:
        form = AtendimentoAmbulatorialForm(instance=atendimento)

    return render(request, "atendimentos/editar.html", {"form": form, "atendimento": atendimento})

# 🔹 Excluir Atendimento
def excluir_atendimento(request, atendimento_id):
    atendimento = get_object_or_404(AtendimentoAmbulatorial, id=atendimento_id)
    atendimento.delete()
    messages.success(request, "🗑️ Atendimento excluído com sucesso!")
    return redirect("listar_atendimentos")

def dashboard_atendimentos(request):
    # Somando os valores acumulados do ano
    total_atendimentos_ano = AtendimentoAmbulatorial.objects.aggregate(Sum("qtde_atendimentos"))["qtde_atendimentos__sum"] or 0
    total_remocoes_ano = AtendimentoAmbulatorial.objects.aggregate(Sum("qtde_remocoes"))["qtde_remocoes__sum"] or 0
    total_clientes_ano = AtendimentoAmbulatorial.objects.aggregate(Sum("qtde_clientes"))["qtde_clientes__sum"] or 0
    total_lojistas_ano = AtendimentoAmbulatorial.objects.aggregate(Sum("qtde_lojistas"))["qtde_lojistas__sum"] or 0
    total_homens_ano = AtendimentoAmbulatorial.objects.aggregate(Sum("qtde_homens"))["qtde_homens__sum"] or 0
    total_mulheres_ano = AtendimentoAmbulatorial.objects.aggregate(Sum("qtde_mulheres"))["qtde_mulheres__sum"] or 0

    # Criando a lista de indicadores para os cartões
    indicadores = [
        {"titulo": "Acumulado", "valor": total_atendimentos_ano, "icone": "📅"},
        {"titulo": "Remoções", "valor": total_remocoes_ano, "icone": "🚑"},
        {"titulo": "Clientes", "valor": total_clientes_ano, "icone": "👨‍👩‍👦"},
        {"titulo": "Lojistas", "valor": total_lojistas_ano, "icone": "🏬"},
        {"titulo": "Homens", "valor": total_homens_ano, "icone": "🧑"},
        {"titulo": "Mulheres", "valor": total_mulheres_ano, "icone": "👩"},
    ]

    # Dados do gráfico
    dados_mensais = AtendimentoAmbulatorial.objects.values("mes").annotate(total_atendimentos=Sum("qtde_atendimentos")).order_by("mes")
    meses = [item["mes"] for item in dados_mensais]
    total_atendimentos = [item["total_atendimentos"] for item in dados_mensais]

    context = {
        "meses": json.dumps(meses),
        "total_atendimentos": json.dumps(total_atendimentos),
        "indicadores": indicadores,
    }

    return render(request, "atendimentos/dashboard.html", context)

def cadastrar_colaborador(request):
    """Cadastra um novo colaborador."""
    if request.method == "POST":
        form = ColaboradorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Colaborador cadastrado com sucesso!")
            return redirect("listar_usuarios")  # 🔹 Redireciona para a lista de colaboradores
        else:
            messages.error(request, "❌ Erro ao cadastrar colaborador. Verifique os dados.")
    else:
        form = ColaboradorForm()

    return render(request, "colaboradores/cadastrar_colaborador.html", {"form": form})

def listar_usuarios(request):
    """ Lista todos os colaboradores cadastrados e permite filtrar pelo nome """
    busca = request.GET.get("busca", "").strip()

    if busca:
        colaboradores = Colaborador.objects.filter(nome_completo__icontains=busca)
    else:
        colaboradores = Colaborador.objects.all()

    return render(request, "usuarios/listar_usuarios.html", {"colaboradores": colaboradores})


def editar_usuario(request, usuario_id):
    """ Edita um colaborador cadastrado """
    colaborador = get_object_or_404(Colaborador, id=usuario_id)

    if request.method == "POST":
        form = ColaboradorForm(request.POST, instance=colaborador)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Usuário atualizado com sucesso!")
            return redirect("listar_usuarios")
    else:
        form = ColaboradorForm(instance=colaborador)

    return render(request, "usuarios/editar_usuario.html", {"form": form})

def deletar_usuario(request, usuario_id):
    """ Remove um colaborador do banco de dados """
    colaborador = get_object_or_404(Colaborador, id=usuario_id)
    colaborador.delete()
    messages.success(request, "❌ Usuário removido com sucesso!")
    return redirect("listar_usuarios")

def buscar_dados_colaborador(request):
    """ Busca automaticamente e-mail e telefone do colaborador ao selecionar um nome """
    colaborador_id = request.GET.get("colaborador_id")
    colaborador = get_object_or_404(Colaborador, id=colaborador_id)
    
    data = {
        "email": colaborador.email,
        "telefone": colaborador.telefone
    }
    
    return JsonResponse(data)