from django import forms
from control.models import Movimentacao, Deposito, Pedidos_Compra

class MovimentacaoForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = "__all__"

class DepositoForm(forms.ModelForm):
    class Meta:
        model = Deposito
        fields = "__all__"

class Pedidos_CompraForm(forms.ModelForm):
    class Meta:
        model = Pedidos_Compra
        fields = "__all__"

