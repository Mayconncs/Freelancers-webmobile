from django import forms
from freelancer.models import Perfil
from freelancer.consts import OPCOES_HABILIDADES

class FormularioPerfil(forms.ModelForm):
    habilidades = forms.MultipleChoiceField(
        choices=OPCOES_HABILIDADES,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Perfil
        exclude = ['usuario']
        widgets = {
            'papel': forms.Select(attrs={'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'localizacao': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_habilidades(self):
        habilidades = self.cleaned_data.get('habilidades', [])
        valid_ids = [id for id, _ in OPCOES_HABILIDADES]
        habilidades = [int(h) for h in habilidades]
        if not all(h in valid_ids for h in habilidades):
            raise forms.ValidationError("Habilidade inválida selecionada.")
        return habilidades