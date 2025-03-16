from django import forms
from .models import MovimentacaoChave
from django import forms
from .models import Chave
from django import forms
from .models import ReciclagemVigilante
from django import forms
from .models import DocumentoFundamental
from django import forms
from .models import AtendimentoAmbulatorial

class MovimentacaoChaveForm(forms.ModelForm):
    class Meta:
        model = MovimentacaoChave
        fields = ["chave", "responsavel", "telefone", "email", "data_saida", "horario_saida", "operador_saida"]  # ✅ Adicionado 'email'
        widgets = {
            "chave": forms.Select(attrs={"class": "form-control"}),
            "responsavel": forms.TextInput(attrs={"class": "form-control"}),
            "telefone": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),  # ✅ Adicionado EmailInput
            "data_saida": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "horario_saida": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "operador_saida": forms.TextInput(attrs={"class": "form-control"}),
        }
    
class ChaveForm(forms.ModelForm):
    class Meta:
        model = Chave
        fields = ["numero", "nome", "cor_chaveiro"]
        labels = {
            "numero": "Número da Chave",
            "nome": "Nome da Chave",
            "cor_chaveiro": "Cor do Chaveiro",
        }
        widgets = {
            "numero": forms.TextInput(attrs={"class": "form-control"}),
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "cor_chaveiro": forms.TextInput(attrs={"class": "form-control"}),
        }

class ReciclagemVigilanteForm(forms.ModelForm):
    class Meta:
        model = ReciclagemVigilante
        fields = ["nome_colaborador", "data_ultima_reciclagem", "diploma"]
        widgets = {
            "nome_colaborador": forms.TextInput(attrs={"class": "form-control"}),
            "data_ultima_reciclagem": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "diploma": forms.FileInput(attrs={"class": "form-control"}),
        }


class DocumentoFundamentalForm(forms.ModelForm):
    class Meta:
        model = DocumentoFundamental
        fields = [
            "nome_documento", "emissao", "vencimento", "entidade_emissora", 
            "funcao_documento", "area", "arquivo"
        ]  # 🔹 Removido o "validade"
        widgets = {
            "emissao": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "vencimento": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["validade"] = forms.IntegerField(
                required=False,
                widget=forms.NumberInput(attrs={"class": "form-control", "readonly": "readonly"})
            )

class AtendimentoAmbulatorialForm(forms.ModelForm):
    class Meta:
        model = AtendimentoAmbulatorial
        fields = "__all__"  # 🔹 Inclui todos os campos no formulário
        widgets = {
            "data": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "mes": forms.TextInput(attrs={"class": "form-control"}),
            "trimestre": forms.NumberInput(attrs={"class": "form-control"}),
            "ano": forms.NumberInput(attrs={"class": "form-control"}),
            "qtde_atendimentos": forms.NumberInput(attrs={"class": "form-control"}),
            "qtde_chamados": forms.NumberInput(attrs={"class": "form-control"}),
            "qtde_remocoes": forms.NumberInput(attrs={"class": "form-control"}),
            "resolvidos": forms.NumberInput(attrs={"class": "form-control"}),
            "qtde_clientes": forms.NumberInput(attrs={"class": "form-control"}),
            "qtde_lojistas": forms.NumberInput(attrs={"class": "form-control"}),
            "qtde_homens": forms.NumberInput(attrs={"class": "form-control"}),
            "qtde_mulheres": forms.NumberInput(attrs={"class": "form-control"}),
            "ambulatorial": forms.NumberInput(attrs={"class": "form-control"}),
            "traumatologico": forms.NumberInput(attrs={"class": "form-control"}),
            "colaboradores_terceiros": forms.NumberInput(attrs={"class": "form-control"}),
            "colaboradores_organicos": forms.NumberInput(attrs={"class": "form-control"}),
            "prestadores_servico": forms.NumberInput(attrs={"class": "form-control"}),
        }
