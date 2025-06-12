from django import forms
from projeto.models import Projeto
from freelancer.consts import OPCOES_HABILIDADES

class FormularioProjeto(forms.ModelForm):
    habilidades_requeridas = forms.MultipleChoiceField(
        choices=OPCOES_HABILIDADES,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Projeto
        exclude = ['cliente', 'data_criacao']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control'}),
            'localizacao': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_habilidades_requeridas(self):
        habilidades = self.cleaned_data.get('habilidades_requeridas', [])
        # Converte strings para inteiros
        return [int(h) for h in habilidades]