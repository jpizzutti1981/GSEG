from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from controle_chaves.models import MovimentacaoChave

class Command(BaseCommand):
    help = "Envia e-mail para responsáveis que não devolveram a chave após 24h."

    def handle(self, *args, **kwargs):
        agora = datetime.now()
        limite_24h = agora - timedelta(hours=24)  # ✅ Agora considera exatamente 24h atrás

        # 🔍 Busca chaves que NÃO foram devolvidas e passaram de 24h desde a retirada
        chaves_atrasadas = MovimentacaoChave.objects.filter(
            status__iexact="Não Devolvida",
            data_saida__lte=limite_24h  # ✅ Agora verifica exatamente a data + hora correta
        )

        # 🚨 Se não houver chaves atrasadas, interrompe o script
        if not chaves_atrasadas.exists():
            self.stdout.write(self.style.WARNING("🚨 Nenhuma chave está atrasada. Nenhuma notificação enviada."))
            return

        # 🔹 Enviar e-mails apenas para chaves que passaram de 24h
        for chave in chaves_atrasadas:
            if chave.email:
                self.enviar_email(chave.responsavel, chave.email, chave.chave.numero, chave.data_saida)

        self.stdout.write(self.style.SUCCESS(f"📨 {chaves_atrasadas.count()} notificações enviadas."))

    def enviar_email(self, responsavel, email, numero_chave, data_saida):
        try:
            assunto = "🔑 Aviso de Chave Atrasada"
            corpo = f"""
            Olá {responsavel},

            A chave {numero_chave} retirada em {data_saida.strftime('%d/%m/%Y às %H:%M')} ainda não foi devolvida.

            Por favor, regularize essa situação o quanto antes.

            Se já devolveu, desconsidere este e-mail.

            Atenciosamente,
            Equipe Central de Segurança
            """

            send_mail(
                assunto,
                corpo,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False
            )

            self.stdout.write(self.style.SUCCESS(f"✅ E-mail enviado para {responsavel} ({email})"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Falha ao enviar e-mail: {e}"))
