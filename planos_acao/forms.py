from django import forms
from .models import PlanoAcao
from ocorrencias.models import Ocorrencia

class PlanoAcaoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        queryset = Ocorrencia.objects.filter(status__iexact='pendente')
        self.fields['ocorrencia'].queryset = queryset
        self.fields['ocorrencia'].required = False
        self.fields['ocorrencia'].empty_label = None
        self.fields['ocorrencia'].choices = list(self.fields['ocorrencia'].choices) + [('outro', 'Outro')]

    class Meta:
        model = PlanoAcao
        fields = ['ocorrencia', 'descricao', 'responsavel', 'prazo', 'status']
        widgets = {
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'responsavel': forms.TextInput(attrs={'class': 'form-control'}),
            'prazo': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'ocorrencia': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_ocorrencia(self):
        data = self.cleaned_data.get('ocorrencia')
        # Se o valor for 'outro', ignoramos o campo
        if data == 'outro':
            return None
        return data
