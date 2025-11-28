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
    
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria_Produto
        fields = "__all__"

class PedidosVendaForm(forms.ModelForm):
    class Meta:
        model = Pedidos_Venda
        fields = "__all__"