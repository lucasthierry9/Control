from django import forms
from . models import Cliente, Produto, Funcionario, Vendedor, Fornecedor, Usuario
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['nome','email','empresa','cpf_cnpj','telefone' ]

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = "__all__"

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = "__all__"

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = "__all__"

class VendedorForm(forms.ModelForm):
    class Meta:
        model = Vendedor
        fields = "__all__"

class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = "__all__"