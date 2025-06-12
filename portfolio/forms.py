from django import forms
from portfolio.models import Portfolio

class FormularioPortfolio(forms.ModelForm):
    class Meta:
        model = Portfolio
        exclude = ['freelancer']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control'}),
            'imagens': forms.FileInput(attrs={'class': 'form-control'}),
            'links': forms.URLInput(attrs={'class': 'form-control'}),
        }