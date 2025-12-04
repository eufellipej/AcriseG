from django import forms
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from .models import Usuario

class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu email'
        })
    )
    senha = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua senha'
        })
    )

class RegistroForm(forms.ModelForm):
    senha = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua senha'
        }),
        validators=[validate_password],
        help_text="Sua senha deve conter pelo menos 8 caracteres, incluindo letras e números."
    )
    confirmar_senha = forms.CharField(
        label="Confirmar Senha",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme sua senha'
        })
    )
    
    class Meta:
        model = Usuario
        fields = ['nome', 'email', 'imagem']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite seu nome completo'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite seu email'
            }),
            'imagem': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }
        help_texts = {
            'imagem': 'Imagem de perfil (opcional)',
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email já está registrado.")
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha")
        confirmar_senha = cleaned_data.get("confirmar_senha")
        
        if senha and confirmar_senha and senha != confirmar_senha:
            self.add_error('confirmar_senha', "As senhas não coincidem.")
        
        return cleaned_data
    
    def save(self, commit=True):
        usuario = super().save(commit=False)
        # Hash da senha antes de salvar
        usuario.senha = make_password(self.cleaned_data["senha"])
        
        if commit:
            usuario.save()
        return usuario

class AtualizarPerfilForm(forms.ModelForm):
    """Formulário para atualizar o perfil do usuário"""
    class Meta:
        model = Usuario
        fields = ['nome', 'imagem']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite seu nome completo'
            }),
            'imagem': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }

class AlterarSenhaForm(forms.Form):
    """Formulário para alteração de senha"""
    senha_atual = forms.CharField(
        label="Senha Atual",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua senha atual'
        })
    )
    nova_senha = forms.CharField(
        label="Nova Senha",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua nova senha'
        }),
        validators=[validate_password]
    )
    confirmar_nova_senha = forms.CharField(
        label="Confirmar Nova Senha",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme sua nova senha'
        })
    )
    
    def __init__(self, usuario=None, *args, **kwargs):
        self.usuario = usuario
        super().__init__(*args, **kwargs)
    
    def clean(self):
        cleaned_data = super().clean()
        nova_senha = cleaned_data.get("nova_senha")
        confirmar_nova_senha = cleaned_data.get("confirmar_nova_senha")
        
        if nova_senha and confirmar_nova_senha and nova_senha != confirmar_nova_senha:
            self.add_error('confirmar_nova_senha', "As senhas não coincidem.")
        
        return cleaned_data