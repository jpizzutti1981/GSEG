from django import forms
from .models import Ocorrencia, TipoOcorrencia, Local
from django import forms
from .models import ConfiguracaoAutomacao
from django import forms

class OcorrenciaForm(forms.ModelForm):
    horario = forms.TimeField(
        widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        input_formats=['%H:%M']
    )

    class Meta:
        model = Ocorrencia
        fields = ['data_ocorrencia', 'horario', 'tipo', 'status', 'local', 'nome_local', 'relato', 'imagem', 'responsavel', 'envolvidos', 'acoes_tomadas', 'supervisor']
        widgets = {
            'data_ocorrencia': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(choices=Ocorrencia.STATUS_CHOICES, attrs={'class': 'form-select'}),
            'local': forms.Select(attrs={'class': 'form-select'}),
            'nome_local': forms.TextInput(attrs={'class': 'form-control'}),
            'relato': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'imagem': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'responsavel': forms.TextInput(attrs={'class': 'form-control'}),
            'envolvidos': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'acoes_tomadas': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'supervisor': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ConfiguracaoAutomacaoForm(forms.ModelForm):
    class Meta:
        model = ConfiguracaoAutomacao
        fields = ['emails_destinatarios', 'assunto', 'mensagem', 'horario_envio']


