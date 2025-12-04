from django import forms
from control.models import Pedidos_Venda

class PedidosVendaForm(forms.ModelForm):
    class Meta:
        model = Pedidos_Venda
        fields = "__all__"