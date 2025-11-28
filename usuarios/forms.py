from . models import Usuario
from django.contrib.auth.forms import UserCreationForm

class UserForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['razao_social','nome_fantasia','cnpj', 'email', 'telefone' ]
        