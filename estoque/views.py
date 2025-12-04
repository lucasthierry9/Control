from django.shortcuts import render,get_object_or_404, redirect
from control.models import Movimentacao, Deposito, Pedidos_Compra, Estoque_Produto, Produto
from . forms import MovimentacaoForm, DepositoForm, Pedidos_CompraForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum

#MOVIMENTAÇÕES
@login_required
def movimentacoes(request):
    ordenar = request.GET.get("ordenar")
    if ordenar:
        movimentacoes = Movimentacao.objects.all().order_by(ordenar)
    else:
        movimentacoes = Movimentacao.objects.all().order_by('-id')

    paginator = Paginator(movimentacoes, 10)
    numero_da_pagina = request.GET.get('p')
    movimentacoes_paginados = paginator.get_page(numero_da_pagina)
    return render(request, "estoque/movimentacoes/movimentacoes.html", {"movimentacoes": movimentacoes_paginados})

@login_required
def adicionar_movimentacao(request):
    if request.method == "POST":
        form = MovimentacaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("estoque:movimentacoes")
    else:
        form = MovimentacaoForm()
    return render(request, "estoque/movimentacoes/adicionar_movimentacao.html", {"form": form})

#VERIFICAÇÃO
@login_required
def verificacao(request):
    depositos = Deposito.objects.all()
    resultado = None

    deposito_id = request.GET.get("deposito")
    codigo = request.GET.get("codigo")

    if codigo:
        try:
            produto = Produto.objects.get(id=codigo)

            if deposito_id == "todos":
                quant = Estoque_Produto.objects.filter(produto=produto).aggregate(total=Sum('quantidade'))['total'] or 0
            else:
                quant = Estoque_Produto.objects.get(produto=produto, deposito_id=deposito_id).quantidade

            resultado = {
                "produto": produto,
                "quantidade": quant,
            }

        except Produto.DoesNotExist:
            resultado = "nenhum_produto"
        except Estoque_Produto.DoesNotExist:
            resultado = "sem_estoque"

    return render(request, "estoque/verificacao/verificacao.html", {
        "depositos": depositos,
        "resultado": resultado,
    })


#DEPÓSITOS
@login_required
def depositos(request):
    ordenar = request.GET.get("ordenar")
    if ordenar:
        depositos = Deposito.objects.all().order_by(ordenar)
    else:
        depositos = Deposito.objects.all().order_by('-id')

    paginator = Paginator(depositos, 10)
    numero_da_pagina = request.GET.get('p')
    depositos_paginados = paginator.get_page(numero_da_pagina)
    return render(request, "estoque/depositos/depositos.html", {"depositos": depositos_paginados})

@login_required
def adicionar_deposito(request):
    if request.method == "POST":
        form = DepositoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("estoque:depositos")
    else:
        form = DepositoForm()
    return render(request, "estoque/depositos/adicionar_deposito.html", {"form": form})

@login_required
def excluir_deposito(request, id_deposito=0):
    if request.method == "POST":
        ids = request.POST.getlist("ids_selecionados")
        Deposito.objects.filter(id__in=ids).delete() 
        return redirect('estoque:depositos')
    else:
        deposito = get_object_or_404(Deposito, id=id_deposito)
        return render(request, "estoque/depositos/confirma.html", {"deposito": deposito})

#PEDIDOS DE COMPRA
@login_required
def pedidos_compra(request):
    ordenar = request.GET.get("ordenar")
    if ordenar:
        pedidos_compra = Pedidos_Compra.objects.all().order_by(ordenar)
    else:
        pedidos_compra = Pedidos_Compra.objects.all().order_by('-id')

    paginator = Paginator(pedidos_compra, 10)
    numero_da_pagina = request.GET.get('p')
    pedidos_compra_paginados = paginator.get_page(numero_da_pagina)
    return render(request, "estoque/pedidos_compra/pedidos_compra.html", {"pedidos_compra": pedidos_compra_paginados})

@login_required
def adicionar_pedidos_compra(request):
    if request.method == "POST":
        form = Pedidos_CompraForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("estoque:pedidos_compra")
    else:
        form = Pedidos_CompraForm()
    return render(request, "estoque/pedidos_compra/adicionar_pedido_compra.html", {"form": form})


