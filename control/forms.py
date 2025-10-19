from django import forms
from . models import Cliente, Produto, Funcionario

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