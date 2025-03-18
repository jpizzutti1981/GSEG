from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Count
from django.http import HttpResponse
import json
import io
import os
import calendar
from datetime import datetime
import requests

# Importação do ReportLab para geração de PDFs
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.utils import ImageReader

# Importação dos modelos
from .models import Ocorrencia, TipoOcorrencia, Local, ConfiguracaoAutomacao, LogSinopse
from .forms import OcorrenciaForm, ConfiguracaoAutomacaoForm
from django.shortcuts import render, redirect
from .forms import ConfiguracaoAutomacaoForm
from django.contrib import messages
from django.http import JsonResponse
from datetime import timedelta
import json
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
import json
import os
from datetime import datetime

from django.core.mail import send_mail
from django.conf import settings

from .models import Ocorrencia, TipoOcorrencia, Local, ConfiguracaoAutomacao, Agendamento
from .forms import OcorrenciaForm, ConfiguracaoAutomacaoForm
import subprocess

import subprocess
from datetime import time
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ConfiguracaoAutomacao
from .utils import enviar_mensagem_telegram 

import os
import io
from datetime import datetime, timedelta
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from ocorrencias.models import Ocorrencia

from django.shortcuts import render, redirect
from django.conf import settings
import requests
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from datetime import datetime
from django.shortcuts import render
from django.db.models import Count
import json
import locale
from .models import Ocorrencia, TipoOcorrencia

import locale
import json
from datetime import datetime
from django.utils.translation import gettext as _
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Ocorrencia, TipoOcorrencia  # Certifique-se de que os modelos estão corretos

import io
import os
import tempfile
import requests
from datetime import datetime, timedelta
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from ocorrencias.models import Ocorrencia

# -----------------------------------------------------------------------------
# 📌 LOGIN (Exibe mensagens de erro corretamente)
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login realizado com sucesso!")
            return redirect("listar_ocorrencias")
        else:
            messages.error(request, "Usuário ou senha inválidos. Tente novamente.")

    return render(request, "login.html")


# -----------------------------------------------------------------------------
# 📌 LOGOUT
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Você saiu do sistema.")
    return redirect("login")


# -----------------------------------------------------------------------------
# 📌 LISTAR OCORRÊNCIAS (Protegido por login)
@login_required
def listar_ocorrencias(request):
    ocorrencias = Ocorrencia.objects.all()

    # Captura os filtros do usuário
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    tipo_filtro = request.GET.get('tipo', '')
    status_filtro = request.GET.get('status', '')
    local_filtro = request.GET.get('local', '')

    if data_inicio and data_fim:
        ocorrencias = ocorrencias.filter(data_ocorrencia__range=[data_inicio, data_fim])
    elif data_inicio:
        ocorrencias = ocorrencias.filter(data_ocorrencia__gte=data_inicio)
    elif data_fim:
        ocorrencias = ocorrencias.filter(data_ocorrencia__lte=data_fim)

    if tipo_filtro:
        ocorrencias = ocorrencias.filter(tipo_id=tipo_filtro)
    if status_filtro:
        ocorrencias = ocorrencias.filter(status=status_filtro)
    if local_filtro:
        ocorrencias = ocorrencias.filter(local_id=local_filtro)

    tipos = TipoOcorrencia.objects.all()
    locais = Local.objects.all()

    return render(request, 'ocorrencias/listar_ocorrencias.html', {
        'ocorrencias': ocorrencias,
        'tipos': tipos,
        'locais': locais,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'tipo_filtro': tipo_filtro,
        'status_filtro': status_filtro,
        'local_filtro': local_filtro,
    })


# -----------------------------------------------------------------------------
# 📌 CADASTRAR NOVA OCORRÊNCIA (com suporte para upload de imagem)
@login_required
def cadastrar_ocorrencia(request):
    if request.method == "POST":
        form = OcorrenciaForm(request.POST, request.FILES)
        if form.is_valid():
            ocorrencia = form.save(commit=False)

            # ✅ 🔹 Garante que o horário está correto antes de salvar
            if isinstance(ocorrencia.horario, str):
                try:
                    ocorrencia.horario = datetime.strptime(ocorrencia.horario, "%H:%M").time()
                except ValueError:
                    ocorrencia.horario = None  # Se der erro, evita salvar inválido

            ocorrencia.save()

            # 📌 Criar a mensagem para o Telegram
            mensagem = (
                f"🚨 <b>Nova Ocorrência Registrada</b> 🚨\n"
                f"👮‍♂️ Tipo: {ocorrencia.tipo}\n"
                f"📅 Data: {ocorrencia.data_ocorrencia.strftime('%d/%m/%Y')}\n"
                f"🕒 Horário: {ocorrencia.horario.strftime('%H:%M')}\n"
                f"📍 Local: {ocorrencia.local}\n"
                f"📝 Relato: {ocorrencia.relato}\n"
                f"🎯 Ações Tomadas: {ocorrencia.acoes_tomadas}\n"
                f"👨‍💼 Responsável: {ocorrencia.supervisor}"
            )

            # 📌 Pega a URL da imagem corretamente
            imagem_url = None
            if ocorrencia.imagem:
                imagem_url = ocorrencia.imagem.url

            # 📌 Envia a mensagem para o grupo do Telegram
            enviar_mensagem_telegram(mensagem, imagem_url)

            messages.success(request, "Ocorrência cadastrada e enviada para o grupo do Telegram!")
            return redirect('listar_ocorrencias')

    else:
        form = OcorrenciaForm()

    return render(request, 'ocorrencias/cadastrar_ocorrencia.html', {'form': form})

# 📌 EDITAR OCORRÊNCIA
@login_required
def editar_ocorrencia(request, pk):
    ocorrencia = get_object_or_404(Ocorrencia, pk=pk)
    
    if request.method == "POST":
        form = OcorrenciaForm(request.POST, request.FILES, instance=ocorrencia)
        if form.is_valid():
            if "horario" not in form.cleaned_data or not form.cleaned_data["horario"]:
                form.cleaned_data["horario"] = ocorrencia.horario  # 🔹 Mantém o horário antigo
            form.save()
            messages.success(request, "Ocorrência atualizada com sucesso!")
            return redirect('listar_ocorrencias')
        else:
            messages.error(request, "Erro ao salvar a ocorrência. Verifique os dados.")
    else:
        form = OcorrenciaForm(instance=ocorrencia)

    return render(request, "ocorrencias/editar_ocorrencia.html", {"form": form, "ocorrencia": ocorrencia})

# -----------------------------------------------------------------------------
@login_required
def excluir_ocorrencia(request, pk):
    ocorrencia = get_object_or_404(Ocorrencia, pk=pk)
    if request.method == "POST":
        ocorrencia.delete()
        return redirect('listar_ocorrencias')
    return render(request, 'ocorrencias/excluir_ocorrencia.html', {'ocorrencia': ocorrencia})

# -----------------------------------------------------------------------------
# 📌 **Força a codificação correta para evitar erros de Unicode**
try:
    locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")
except locale.Error:
    locale.setlocale(locale.LC_TIME, "C")

@login_required
def dashboard(request):
    mes_filtro = request.GET.get('mes', '')
    ano_filtro = request.GET.get('ano', '')
    tipo_filtro = request.GET.get('tipo', '')
    status_filtro = request.GET.get('status', '')

    # Filtragem dinâmica
    ocorrencias = Ocorrencia.objects.all()
    if mes_filtro:
        ocorrencias = ocorrencias.filter(data_ocorrencia__month=mes_filtro)
    if ano_filtro:
        ocorrencias = ocorrencias.filter(data_ocorrencia__year=ano_filtro)
    if tipo_filtro:
        ocorrencias = ocorrencias.filter(tipo_id=tipo_filtro)
    if status_filtro:
        ocorrencias = ocorrencias.filter(status=status_filtro)

    # Totais
    total_ocorrencias_mes = ocorrencias.count() if mes_filtro else Ocorrencia.objects.filter(data_ocorrencia__month=datetime.today().month).count()
    total_ocorrencias_ano = ocorrencias.count() if ano_filtro else Ocorrencia.objects.filter(data_ocorrencia__year=datetime.today().year).count()
    total_concluidas = ocorrencias.filter(status="concluido").count()
    total_em_andamento = ocorrencias.filter(status="em_andamento").count()

    # 📌 **Correção definitiva: Obtém os meses sem problemas de encoding**
    meses_traduzidos = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
        5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
        9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }

    ocorrencias_por_mes = (
        ocorrencias.values('data_ocorrencia__month')
        .annotate(total=Count('id'))
        .order_by('data_ocorrencia__month')
    )

    meses_labels = [meses_traduzidos[item['data_ocorrencia__month']] for item in ocorrencias_por_mes]
    meses_values = [item['total'] for item in ocorrencias_por_mes]

    # Disponibilidade de filtros
    meses_disponiveis = meses_traduzidos
    anos_disponiveis = sorted(set(Ocorrencia.objects.values_list('data_ocorrencia__year', flat=True)), reverse=True)

    context = {
        'total_ocorrencias_mes': total_ocorrencias_mes,
        'total_ocorrencias_ano': total_ocorrencias_ano,
        'total_concluidas': total_concluidas,
        'total_em_andamento': total_em_andamento,
        'meses_labels': json.dumps(meses_labels, ensure_ascii=False),
        'meses_values': json.dumps(meses_values),
        'meses_disponiveis': meses_disponiveis,
        'anos_disponiveis': anos_disponiveis,
        'tipos': TipoOcorrencia.objects.all(),
        'mes_filtro': mes_filtro,
        'ano_filtro': ano_filtro,
        'tipo_filtro': tipo_filtro,
        'status_filtro': status_filtro,
    }

    return render(request, 'ocorrencias/dashboard.html', context)
# -----------------------------------------------------------------------------
# 📌 Página da Sinopse com filtros de data
@login_required
def sinopse(request):
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    ocorrencias = None
    if data_inicio and data_fim:
        ocorrencias = Ocorrencia.objects.filter(data_ocorrencia__range=[data_inicio, data_fim]).order_by('horario')
    return render(request, 'ocorrencias/sinopse.html', {
        'ocorrencias': ocorrencias,
        'data_inicio': data_inicio,
        'data_fim': data_fim
    })

# -----------------------------------------------------------------------------
# 📌 Gerar Sinopse 
def gerar_sinopse_pdf(request=None, data_inicio=None, data_fim=None):
    buffer = io.BytesIO()
    elements = []
    styles = getSampleStyleSheet()

    # 🔹 Verificar diretório temporário para salvar PDF
    temp_dir = "/tmp" if os.name != "nt" else os.environ.get("TEMP", "C:\\Temp")
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # 🔹 Definir datas (assume dia anterior se não for fornecido)
    if not data_inicio or not data_fim:
        ontem = datetime.today() - timedelta(days=1)
        data_inicio = data_fim = ontem.strftime("%Y-%m-%d")

    data_formatada = datetime.strptime(data_inicio, "%Y-%m-%d").strftime("%d/%m/%Y")
    data_nome_arquivo = datetime.strptime(data_inicio, "%Y-%m-%d").strftime("%d-%m-%Y")
    nome_arquivo_pdf = f"Sinopse_Diária_{data_nome_arquivo}.pdf"
    caminho_pdf = os.path.join(temp_dir, nome_arquivo_pdf)

    # 🔹 Criar documento PDF
    doc = SimpleDocTemplate(caminho_pdf, pagesize=letter)

    # 🔹 Definir caminhos dos logos
    logo_esquerdo = os.path.join(settings.STATIC_ROOT, "images", "logo.png")
    logo_direito = os.path.join(settings.STATIC_ROOT, "images", "logoad3.png")

    # 🔹 Adicionar cabeçalho com os logos
    header_data = [
        [Image(logo_esquerdo, width=120, height=50),
         Paragraph(f"<b>SINOPSE DIÁRIA - {data_formatada}</b>", styles["Title"]),
         Image(logo_direito, width=80, height=50)]
    ]
    header_table = Table(header_data, colWidths=[150, 250, 150])
    header_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 15))

    # 🔹 Buscar Ocorrências
    ocorrencias = Ocorrencia.objects.filter(data_ocorrencia__range=[data_inicio, data_fim])
    imagens_temp = []

    for ocorrencia in ocorrencias:
        elements.append(Spacer(1, 10))
        elements.append(Paragraph(f"<b>ID:</b> {ocorrencia.id} - <b>{ocorrencia.tipo}</b> | {ocorrencia.local}", styles["Title"]))
        elements.append(Spacer(1, 5))

        dados_ocorrencia = [
            ["Data:", ocorrencia.data_ocorrencia.strftime("%d/%m/%Y")],
            ["Horário:", ocorrencia.horario.strftime("%H:%M")],
            ["Relato:", Paragraph(ocorrencia.relato, styles["Normal"])],
            ["Ações Tomadas:", Paragraph(ocorrencia.acoes_tomadas, styles["Normal"])],
            ["Supervisor:", ocorrencia.supervisor],
        ]
        table = Table(dados_ocorrencia, colWidths=[100, 400])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 15))

        # 🔹 Baixar Imagem Temporária
        if ocorrencia.imagem:
            try:
                img_url = ocorrencia.imagem.url
                temp_img = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
                temp_img_path = temp_img.name
                temp_img.close()

                response = requests.get(img_url, stream=True)
                if response.status_code == 200:
                    with open(temp_img_path, "wb") as img_file:
                        for chunk in response.iter_content(1024):
                            img_file.write(chunk)

                    imagens_temp.append(temp_img_path)
                    img = Image(temp_img_path, width=400, height=200)
                    elements.append(img)
                    elements.append(Spacer(1, 20))

            except Exception as e:
                print(f"Erro ao carregar imagem: {e}")

    doc.build(elements)

    # 🔹 Apagar Imagens Temporárias
    for img_path in imagens_temp:
        try:
            os.remove(img_path)
        except Exception as e:
            print(f"⚠ Erro ao deletar imagem temporária: {img_path} - {e}")

    # 🔹 Retornar o PDF gerado
    if request is not None:  
        with open(caminho_pdf, "rb") as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type="application/pdf")
            response["Content-Disposition"] = f'attachment; filename="{nome_arquivo_pdf}"'
            return response
    else:  
        return caminho_pdf

# 📌 CONFIGURAÇÃO DA AUTOMAÇÃO
@login_required
def configuracao_automacao(request):
    configuracao, _ = ConfiguracaoAutomacao.objects.get_or_create(id=1)

    # 🔹 Garante que `horario_envio` nunca seja `None`
    if not configuracao.horario_envio:
        configuracao.horario_envio = "12:00"  # Define um valor padrão
        configuracao.save()

    if request.method == "POST":
        try:
            # 🔹 Captura os valores enviados pelo formulário
            emails_destinatarios = request.POST.get("emails_destinatarios", "").strip()
            assunto = request.POST.get("assunto", "").strip()
            mensagem = request.POST.get("mensagem", "").strip()
            horario_envio = request.POST.get("horario_envio", "12:00").strip()

            # 🔹 Valida os dados
            if not emails_destinatarios:
                messages.error(request, "Erro: Você precisa informar pelo menos um e-mail válido.")
                return redirect("automacao")

            # 🔹 Atualiza a configuração no banco de dados
            configuracao.emails_destinatarios = emails_destinatarios
            configuracao.assunto = assunto
            configuracao.mensagem = mensagem
            configuracao.horario_envio = horario_envio
            configuracao.save()

            # 🔹 Define os caminhos dos arquivos
            caminho_bat = "C:\\Users\\Jorge\\gestao_ocorrencias\\executar_sinopse.bat"
            caminho_vbs = "C:\\Users\\Jorge\\gestao_ocorrencias\\executar_sinopse.vbs"

            # 🔹 Atualiza o arquivo `.bat`
            with open(caminho_bat, "w") as bat_file:
                bat_file.write(f'@echo off\n')
                bat_file.write(f'cd C:\\Users\\Jorge\\gestao_ocorrencias\n')
                bat_file.write(f'call venv\\Scripts\\activate\n')  # `call` evita fechamento imediato
                bat_file.write(f'python manage.py enviar_sinopse\n')

            # 🔹 Atualiza o arquivo `.vbs` para executar o `.bat` sem exibir a janela
            with open(caminho_vbs, "w") as vbs_file:
                vbs_file.write(f'Set WshShell = CreateObject("WScript.Shell")\n')
                vbs_file.write(f'WshShell.Run chr(34) & "{caminho_bat}" & chr(34), 0\n')
                vbs_file.write(f'Set WshShell = Nothing\n')

            # 🔹 Configura o Agendador de Tarefas do Windows para executar o `.vbs` (e não o `.bat`)
            nome_tarefa = "EnviarSinopseDiaria"
            hora, minuto = map(int, horario_envio.split(":"))

            # 🔹 Remove a tarefa antiga caso já exista
            remover_tarefa = f'schtasks /delete /tn "{nome_tarefa}" /f'
            subprocess.run(remover_tarefa, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # 🔹 Cria a nova tarefa com o horário atualizado
            comando_schtasks = f'schtasks /create /tn "{nome_tarefa}" /tr "{caminho_vbs}" /sc daily /st {hora:02d}:{minuto:02d} /RL HIGHEST /F'
            resultado = subprocess.run(comando_schtasks, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # 🔹 Verifica se houve erro no `schtasks`
            if resultado.returncode != 0:
                messages.error(request, f"Erro ao agendar a tarefa: {resultado.stderr}")
                return redirect("automacao")

            messages.success(request, "Configuração salva e agendamento atualizado com sucesso!")
            return redirect("automacao")

        except Exception as e:
            messages.error(request, f"Erro ao salvar: {str(e)}")
            return redirect("automacao")

    return render(request, "ocorrencias/automacao.html", {"configuracao": configuracao})

@login_required
def monitoramento(request):
    logs = LogSinopse.objects.order_by('-data_execucao')[:10]  # Últimos 10 registros
    return render(request, 'ocorrencias/monitoramento.html', {'logs': logs})

# -----------------------------------------------------------------------------

@login_required
def excluir_agendamento(request, agendamento_id):
    agendamento = get_object_or_404(ConfiguracaoAutomacao, id=agendamento_id)
    agendamento.delete()
    messages.success(request, "Agendamento excluído com sucesso!")
    return redirect("automacao")

@login_required
def editar_agendamento(request, agendamento_id):
    agendamento = get_object_or_404(ConfiguracaoAutomacao, id=agendamento_id)

    if request.method == "POST":
        novo_horario = request.POST.get("horario_envio")

        if not novo_horario:
            messages.error(request, "Erro: O horário não pode ser vazio!")
            return redirect("editar_agendamento", agendamento_id=agendamento.id)

        agendamento.horario_envio = novo_horario
        agendamento.save()

        try:
            # 🔹 Atualiza o arquivo .bat para executar o script
            caminho_bat = "C:\\Users\\Jorge\\gestao_ocorrencias\\executar_sinopse.bat"
            with open(caminho_bat, "w") as bat_file:
                bat_file.write(f'@echo off\n')
                bat_file.write(f'cd /d C:\\Users\\Jorge\\gestao_ocorrencias\n')
                bat_file.write(f'call venv\\Scripts\\activate\n')
                bat_file.write(f'python manage.py enviar_sinopse\n')

            # 🔹 Configuração do Agendador de Tarefas do Windows
            nome_tarefa = "EnviarSinopseDiaria"
            hora, minuto = map(int, novo_horario.split(":"))

            # Remove a tarefa anterior, se existir (silencioso)
            subprocess.run(f'schtasks /delete /tn "{nome_tarefa}" /f', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # Cria a nova tarefa agendada (silencioso)
            comando_schtasks = f'schtasks /create /tn "{nome_tarefa}" /tr "{caminho_bat}" /sc daily /st {hora:02d}:{minuto:02d} /f'
            subprocess.run(comando_schtasks, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            messages.success(request, "Agendamento atualizado com sucesso!")

        except Exception as e:
            messages.error(request, f"Erro ao atualizar agendamento: {str(e)}")

        return redirect("automacao")

    return render(request, "ocorrencias/editar_agendamento.html", {"agendamento": agendamento})

@login_required
def teste_envio_email(request):
    try:
        destinatarios = ["jgcanil@hotmail.com"]  # Adicione um destinatário de teste fixo
        assunto = "Teste de Envio de E-mail"
        mensagem = "Este é um teste de envio de e-mail pelo sistema de automação."

        send_mail(
            assunto,
            mensagem,
            settings.EMAIL_HOST_USER,
            destinatarios,
            fail_silently=False,
        )

        return JsonResponse({"status": "sucesso", "mensagem": "E-mail de teste enviado com sucesso!"})

    except Exception as e:
        return JsonResponse({"status": "erro", "mensagem": str(e)}, status=500)

@login_required
def listar_agendamentos(request):
    agendamentos = Agendamento.objects.filter(ativo=True)
    return render(request, "ocorrencias/listar_agendamentos.html", {"tarefas": agendamentos})

