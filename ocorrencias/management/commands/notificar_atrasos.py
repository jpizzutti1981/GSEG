import smtplib
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q, F
from controle_chaves.models import MovimentacaoChave

class Command(BaseCommand):
    help = "Envia e-mail para responsáveis que não devolveram a chave após 24h."

    def handle(self, *args, **kwargs):
        agora = datetime.now()  # 🔹 Captura data e hora ATUAL do servidor
        limite_tempo = agora - timedelta(hours=24)  # 🔹 Chaves com MAIS DE 24h

        # 🔹 Filtra chaves atrasadas que ainda não foram devolvidas
        chaves_atrasadas = MovimentacaoChave.objects.filter(
            Q(status__iexact="Não Devolvida"), 
            data_saida__lte=limite_tempo  # 🔹 Agora comparando com data e HORA corretamente
        )

        # 🚨 Se não houver chaves atrasadas, encerra o script
        if not chaves_atrasadas.exists():
            self.stdout.write(self.style.WARNING("🚨 Nenhuma chave está atrasada. Nenhuma notificação enviada."))
            return

        # 🔹 Enviar e-mails para responsáveis
        for chave in chaves_atrasadas:
            if chave.email:  # 🔹 Garante que o e-mail existe
                self.enviar_email(chave.responsavel, chave.email, chave.chave.numero, chave.data_saida)

        self.stdout.write(self.style.SUCCESS(f"📨 {chaves_atrasadas.count()} notificações enviadas."))

    def enviar_email(self, responsavel, email, numero_chave, data_saida):
        try:
            assunto = "🔑 Aviso de Chave Atrasada"
            corpo = f"""
            Olá {responsavel},

            A chave {numero_chave} retirada no dia {data_saida.strftime('%d/%m/%Y %H:%M')} ainda não foi devolvida.

            Por favor, regularize essa situação o quanto antes.

            Se já devolveu, desconsidere este e-mail.

            Atenciosamente,
            Equipe Central de Segurança
            """

            send_mail(
                assunto,
                corpo,
                settings.EMAIL_HOST_USER,  # 🔹 Remetente
                [email],  # 🔹 Destinatário
                fail_silently=False
            )

            self.stdout.write(self.style.SUCCESS(f"✅ E-mail enviado para {responsavel} ({email})"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Falha ao enviar e-mail: {e}"))
