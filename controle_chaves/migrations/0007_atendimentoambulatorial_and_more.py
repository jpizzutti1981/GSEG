# Generated by Django 4.2.19 on 2025-03-15 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controle_chaves', '0006_documentofundamental'),
    ]

    operations = [
        migrations.CreateModel(
            name='AtendimentoAmbulatorial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(verbose_name='Data')),
                ('mes', models.CharField(max_length=20, verbose_name='Mês')),
                ('trimestre', models.IntegerField(verbose_name='Trimestre')),
                ('ano', models.IntegerField(verbose_name='Ano')),
                ('qtde_atendimentos', models.IntegerField(default=0, verbose_name='Qtde Atendimentos')),
                ('qtde_chamados', models.IntegerField(default=0, verbose_name='Qtde Chamados')),
                ('qtde_remocoes', models.IntegerField(default=0, verbose_name='Qtde Remoções')),
                ('resolvidos', models.IntegerField(default=0, verbose_name='Resolvidos')),
                ('qtde_clientes', models.IntegerField(default=0, verbose_name='Qtde Clientes')),
                ('qtde_lojistas', models.IntegerField(default=0, verbose_name='Qtde Lojistas')),
                ('qtde_homens', models.IntegerField(default=0, verbose_name='Qtde Homens')),
                ('qtde_mulheres', models.IntegerField(default=0, verbose_name='Qtde Mulheres')),
                ('ambulatorial', models.IntegerField(default=0, verbose_name='Ambulatorial')),
                ('traumatologico', models.IntegerField(default=0, verbose_name='Traumatológico')),
                ('colaboradores_terceiros', models.IntegerField(default=0, verbose_name='Colaboradores Terceiros')),
                ('colaboradores_organicos', models.IntegerField(default=0, verbose_name='Colaboradores Orgânicos')),
                ('prestadores_servico', models.IntegerField(default=0, verbose_name='Prestadores de Serviço')),
            ],
        ),
        migrations.AlterField(
            model_name='documentofundamental',
            name='area',
            field=models.CharField(choices=[('Segurança', 'Segurança'), ('Administrativo', 'Administrativo'), ('Estacionamento', 'Estacionamento'), ('Operacional', 'Operacional'), ('Outro', 'Outro')], max_length=50, verbose_name='Área'),
        ),
    ]
