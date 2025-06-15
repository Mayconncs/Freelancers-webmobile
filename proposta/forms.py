from django import forms
from proposta.models import Proposta

class FormularioProposta(forms.ModelForm):
    class Meta:
        model = Proposta
        exclude = ['freelancer', 'status']
        widgets = {
            'projeto': forms.HiddenInput(),
            'preco': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Digite o valor da proposta (ex.: 1000.00)'}),
            'tempo_estimado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: 5 dias ou 2 semanas'}),
            'mensagem': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descreva sua proposta e experiência relevante'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        projeto = cleaned_data.get('projeto')
        if projeto and projeto.status != 1:
            raise forms.ValidationError("Propostas só podem ser enviadas para projetos abertos.")
        return cleaned_data