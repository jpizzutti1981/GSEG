from django import forms
from .models import Notificacao

class NotificacaoForm(forms.ModelForm):
    data_ocorrencia = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    hora_ocorrencia = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = Notificacao
        fields = ['data_ocorrencia', 'hora_ocorrencia','loja', 'motivo', 'descricao', 'imagem', 'notificado_por']

#'itens_notificados',