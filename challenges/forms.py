from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
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
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ex: Maratona Python 30 dias',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Descreva a meta do desafio...',
                }
            ),
            'target_days': forms.NumberInput(
                attrs={'class': 'form-control', 'min': 1}
            ),
            'is_public': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }


# Formulário Customizado de Cadastro
class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        label='Nome',
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Seu primeiro nome'}
        ),
    )
    last_name = forms.CharField(
        label='Sobrenome',
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Seu sobrenome'}
        ),
    )
    email = forms.EmailField(
        label='E-mail',
        required=True,
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'seu@email.com'}
        ),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + (
            'first_name',
            'last_name',
            'email',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplica a classe Bootstrap nos campos herdados do UserCreationForm (username e senhas)
        for field in self.fields.values():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
