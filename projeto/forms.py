from django import forms
from projeto.models import Projeto
from freelancer.consts import OPCOES_HABILIDADES

class FormularioProjeto(forms.ModelForm):
    habilidades_requeridas = forms.MultipleChoiceField(
        choices=OPCOES_HABILIDADES,
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'}),
        required=False
    )

    class Meta:
        model = Projeto
        exclude = ['cliente', 'data_criacao']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o título do projeto'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descreva os detalhes do projeto'}),
            'estado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: SP'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite a cidade'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 12345-678'}),
            'lote': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o lote, se aplicável'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_habilidades_requeridas(self):
        habilidades = self.cleaned_data.get('habilidades_requeridas', [])
        valid_ids = [id for id, _ in OPCOES_HABILIDADES]
        habilidades = [int(h) for h in habilidades]
        if not all(h in valid_ids for h in habilidades):
            raise forms.ValidationError("Habilidade inválida selecionada.")
        return habilidades

    def clean_cep(self):
        cep = self.cleaned_data.get('cep', '')
        if cep and not cep.replace('-', '').isdigit():
            raise forms.ValidationError("CEP deve conter apenas números e hífen.")
        return cep