from django import forms
from proposta.models import Proposta

class FormularioProposta(forms.ModelForm):
    class Meta:
        model = Proposta
        exclude = ['freelancer', 'status']
        widgets = {
            'projeto': forms.HiddenInput(), 
            'preco': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'tempo_estimado': forms.TextInput(attrs={'class': 'form-control'}),
            'mensagem': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def clean(self):
        cleaned_data = super().clean()
        projeto = cleaned_data.get('projeto')
        if projeto and projeto.status != 1:
            raise forms.ValidationError("Propostas só podem ser enviadas para projetos abertos.")
        return cleaned_data