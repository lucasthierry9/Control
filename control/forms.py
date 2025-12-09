from django import forms
from . models import Cliente, Produto, Funcionario, Vendedor, Fornecedor, Categoria_Produto, Pedidos_Venda

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = "__all__"

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = "__all__"

class FuncionarioForm(forms.Form):
    nome = forms.CharField(max_length=100)
    email = forms.EmailField()
    telefone = forms.CharField(max_length=20)
    cpf = forms.CharField(max_length=11)
    cargo = forms.CharField(max_length=50)
    senha = forms.CharField(widget=forms.PasswordInput)

class VendedorForm(forms.ModelForm):
    class Meta:
        model = Vendedor
        fields = "__all__"

class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = "__all__"
    
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria_Produto
        fields = "__all__"