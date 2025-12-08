from django.shortcuts import render,get_object_or_404,redirect
from control.models import Pedidos_Venda
from . forms import PedidosVendaForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q


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

#RELATÓRIO DE VENDAS
@login_required
def relatorio_vendas(request):
    ano = request.GET.get("ano")
    mes = request.GET.get("mes")
    search = request.GET.get("search")

    pedidos = Pedidos_Venda.objects.all()

    if ano and ano.isdigit():
        pedidos = pedidos.filter(data__year=ano)

    if mes and mes.isdigit():
        pedidos = pedidos.filter(data__month=mes)


    if search:
        pedidos = pedidos.filter(
            Q(produto__nome__icontains=search) |
            Q(cliente__nome__icontains=search) |
            Q(vendedor__nome__icontains=search) 
        )

    pedidos = pedidos.order_by('-id')

    # Lista de anos disponíveis
    anos_disponiveis = Pedidos_Venda.objects.dates('data', 'year')

    # Lista padrão de meses
    meses_lista = [
        ("1", "Janeiro"), ("2", "Fevereiro"), ("3", "Março"),
        ("4", "Abril"), ("5", "Maio"), ("6", "Junho"),
        ("7", "Julho"), ("8", "Agosto"), ("9", "Setembro"),
        ("10", "Outubro"), ("11", "Novembro"), ("12", "Dezembro")
    ]

    paginator = Paginator(pedidos, 10)
    numero_da_pagina = request.GET.get('p')
    pedidos_paginados = paginator.get_page(numero_da_pagina)
    return render(request, "vendas/relatorio/relatorio_vendas.html", {"pedidos": pedidos_paginados, "anos": [a.year for a in anos_disponiveis], "meses": meses_lista, "ano_selecionado": ano, "mes_selecionado": mes, "search": search,})