import csv
import os
from django.core.management.base import BaseCommand
from controle_chaves.models import Chave

class Command(BaseCommand):
    help = "Importa um arquivo CSV de chaves para o banco de dados."

    def handle(self, *args, **kwargs):
        caminho_csv = "C:/Users/Jorge/gestao_ocorrencias/chaves.csv"

        # Detectar automaticamente o separador do arquivo (vírgula ou tabulação)
        with open(caminho_csv, "r", newline="", encoding="utf-8") as csvfile:
            sample = csvfile.read(1024)  # Lê um pedaço do arquivo para detectar o separador
            csvfile.seek(0)  # Volta ao início do arquivo
            delimiter = "," if "," in sample else "\t"  # Detecta automaticamente

            reader = csv.DictReader(csvfile, delimiter=delimiter)

            contador = 0
            for row in reader:
                try:
                    numero = row["numero"].strip()
                    nome = row["nome"].strip()
                    cor_chaveiro = row["cor_chaveiro"].strip()
                    disponivel = row["disponivel"].strip().lower() in ["true", "1", "sim"]

                    chave, created = Chave.objects.get_or_create(
                        numero=numero,
                        defaults={"nome": nome, "cor_chaveiro": cor_chaveiro, "disponivel": disponivel},
                    )

                    if created:
                        contador += 1
                        self.stdout.write(self.style.SUCCESS(f"✅ Chave {numero} importada!"))
                    else:
                        self.stdout.write(self.style.WARNING(f"⚠️ Chave {numero} já existe!"))

                except KeyError as e:
                    self.stdout.write(self.style.ERROR(f"❌ ERRO: Coluna ausente no CSV → {str(e)}"))

            self.stdout.write(self.style.SUCCESS(f"📌 Importação concluída! {contador} novas chaves adicionadas."))
