from . models import Usuario
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth import authenticate

class UserForm(UserCreationForm):
    razao_social = forms.CharField(label='Razão Social', max_length=200)
    nome_fantasia = forms.CharField(label='Nome fantasia', max_length=200)
    cnpj = forms.CharField(label='CNPJ', max_length=14)
    email = forms.EmailField(label='E-mail')
    telefone = forms.CharField(label='Telefone', max_length=11)
    password1 = forms.CharField( label='Crie sua senha de acesso', help_text='', widget=forms.PasswordInput(attrs={'class': 'form-control',}))
    password2 = forms.CharField( label='Confirmação de senha', help_text='', widget=forms.PasswordInput(attrs={'class': 'form-control',}))
    
    class Meta:
        model = Usuario
        fields = [
            'razao_social', 'nome_fantasia', 'cnpj',
            'email', 'telefone', 'password1',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Estilo padrão para todos os campos
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'style': 'background-color: #E9E9E9; border: none; border-radius: 8px; height: 45px;'
            })
            field.label_suffix = ""       

class ImagemPerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['imagem_perfil']
        widgets = {
            'imagem_perfil': forms.ClearableFileInput(attrs={
                'class': 'form-control rounded-3',
            })
        }