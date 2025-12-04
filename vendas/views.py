from django.shortcuts import render,get_object_or_404,redirect
from control.models import Pedidos_Venda
from . forms import PedidosVendaForm
from django.contrib.auth.decorators import login_required


#PEDIDOS
@login_required
def pedidos(request):
    pedidos = Pedidos_Venda.objects.filter(status__in=['aberto', 'processando'])
    return render(request, "vendas/pedidos/pedidos.html", {"pedidos": pedidos})

@login_required
def registrar_pedido(request):
    if request.method == "POST":
        form = PedidosVendaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("vendas:pedidos")
    else:
        form = PedidosVendaForm()
    return render(request, "vendas/pedidos/registrar_pedido.html", {"form": form})

@login_required      
def editar_pedido(request, id_pedido):
    pedido = get_object_or_404(Pedidos_Venda, id=id_pedido)
    form = PedidosVendaForm(request.POST, instance=pedido)
    if form.is_valid():
        form.save()
        return redirect("vendas:pedidos")
    else:
        form = PedidosVendaForm(instance=pedido)
    return render(request, "vendas/pedidos/editar_pedido.html", {"form": form})

@login_required
def excluir_pedido(request, id_pedido=0):
    if request.method == "POST":
        pedido = get_object_or_404(Pedidos_Venda, id=request.POST.get("id_pedido"))
        pedido.delete()
        return redirect('vendas:pedidos')
    else:
        pedido = get_object_or_404(Pedidos_Venda, id=id_pedido)
        return render(request, "vendas/pedidos/confirma.html", {"pedido": pedido})
    
#HISTÓRICO
@login_required
def historico(request):
    pedidos = Pedidos_Venda.objects.filter(status__in=['concluido', 'cancelado'])
    return render(request, "vendas/historico/historico.html", {"pedidos": pedidos})
