from django import forms
from freelancer.models import Perfil
from freelancer.consts import OPCOES_HABILIDADES

class FormularioPerfil(forms.ModelForm):
    habilidades = forms.MultipleChoiceField(
        choices=OPCOES_HABILIDADES,
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'}),
        required=False
    )

    class Meta:
        model = Perfil
        exclude = ['usuario']
        widgets = {
            'papel': forms.Select(attrs={'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: SP'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12345-678'}),
            'lote': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(11) 91234-5678'}),
            'email_contato': forms.EmailInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_habilidades(self):
        habilidades = self.cleaned_data.get('habilidades', [])
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

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone', '')
        if telefone and not telefone.replace('(', '').replace(')', '').replace('-', '').replace(' ', '').isdigit():
            raise forms.ValidationError("Telefone deve conter apenas números, parênteses, hífen e espaços.")
        return telefone