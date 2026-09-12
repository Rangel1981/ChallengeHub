from django import forms
from .models import Challenge

class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ['title', 'description', 'target_days', 'is_public']
        labels = {
            'title': 'Título do Desafio',
            'description': 'Descrição',
            'target_days': 'Meta de Dias',
            'is_public': 'Tornar Desafio Público?',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Maratona Python 30 dias'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descreva a meta do desafio...'}),
            'target_days': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
