from django.shortcuts import render,get_object_or_404, redirect
from control.models import Movimentacao, Deposito, Pedidos_Compra, Estoque_Produto, Produto
from . forms import MovimentacaoForm, DepositoForm, Pedidos_CompraForm
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.db.models import Q
from control.utils import registrar_acao, ultimas_acoes_modulo
from django.contrib import messages

#MOVIMENTAÇÕES
@login_required
def movimentacoes(request):

    # Total de movimentações:
    total_movimentacoes = Movimentacao.objects.count()
    total_entradas = Movimentacao.objects.filter(tipo="entrada").count()
    total_saidas = Movimentacao.objects.filter(tipo="saida").count()

    search = request.GET.get("search")
    
    movimentacoes = Movimentacao.objects.all()

    if search:
        movimentacoes = movimentacoes.filter(
            Q(tipo__icontains=search) |
            Q(produto__nome__icontains=search) |
            Q(id__icontains=search) 
        )
    
    movimentacoes = movimentacoes.order_by('-id')

    paginator = Paginator(movimentacoes, 10)
    numero_da_pagina = request.GET.get('p')
    movimentacoes_paginados = paginator.get_page(numero_da_pagina)
    return render(request, "estoque/movimentacoes/movimentacoes.html", {
        "movimentacoes": movimentacoes_paginados, 
        "search": search, 
        'historico': ultimas_acoes_modulo(request.user, 'movimentacoes'),
        "total_movimentacoes": total_movimentacoes,
        "total_entradas": total_entradas,
        "total_saidas": total_saidas})

@login_required
def adicionar_movimentacao(request):
    if request.method == "POST":
        form = MovimentacaoForm(request.POST)
        if form.is_valid():
            mov = form.save()

            # Atualiza o estoque automaticamente
            estoque, created = Estoque_Produto.objects.get_or_create(
                produto=mov.produto,
                deposito=mov.deposito,
                defaults={'quantidade': 0}
            )

            if mov.tipo == 'entrada':
                estoque.quantidade += mov.quantidade
            else:
                estoque.quantidade -= mov.quantidade

            estoque.save()

            registrar_acao(
                request.user,
                'movimentacoes',
                f"{mov.get_tipo_display()} de {mov.produto} <strong>registrado</strong>"
            )
            return redirect("estoque:movimentacoes")
    else:
        form = MovimentacaoForm()
    return render(request, "estoque/movimentacoes/adicionar_movimentacao.html", {"form": form, 'historico': ultimas_acoes_modulo(request.user, 'movimentacoes')})

@login_required
def editar_movimentacao(request, id_movimentacao):
    movimentacao = get_object_or_404(Movimentacao, id=id_movimentacao)

    if request.method == "POST":
        form = MovimentacaoForm(request.POST, instance=movimentacao)
        if form.is_valid():
            movimentacao = form.save()

            registrar_acao(
                request.user,
                'movimentacoes',
                f"{movimentacao.produto.nome} - {movimentacao.tipo} editado"
            )
            return redirect("estoque:pedidos_compra")
    else:
        form = Pedidos_CompraForm(instance=movimentacao)

    return render(request, "vendas/pedidos/editar_pedido.html", {"form": form, 'historico': ultimas_acoes_modulo(request.user, 'movimentacoes'), "movimentacao": movimentacao})

@login_required
def excluir_movimentacao(request, id_movimentacao=0):
    if request.method == "POST":
        ids = request.POST.getlist("ids_selecionados")

        quantidade = len(ids)

        if quantidade > 0:
            Movimentacao.objects.filter(id__in=ids).delete() 
            # REGISTRA A AÇÃO
            registrar_acao(
                usuario=request.user,
                modulo='movimentacoes',
                descricao=f'{quantidade} movimentacao(s) excluído(s)'
            ) 
        return redirect('estoque:movimentacoes')
    else:
        movimentacao = get_object_or_404(Movimentacao, id=id_movimentacao)
        return render(request, "cadastros/clientes/confirma.html", {"movimentacao": movimentacao , 'historico': ultimas_acoes_modulo(request.user, 'movimentacoes'),})
    
@login_required
def verificacao(request):
    depositos = Deposito.objects.all()
    produto = None
    quantidade = None
    resultado = None

    deposito_id = request.GET.get("deposito")
    codigo = request.GET.get("codigo")

    if codigo:
        registrar_acao(
            request.user,
            'estoque',
            'Uma verificação de estoque foi realizada'
        )
        if not codigo.isdigit():
            resultado = "codigo_invalido"
        else:
            try:
                produto = Produto.objects.get(id=int(codigo))

                if deposito_id == "todos":
                    quantidade = (
                        Estoque_Produto.objects
                        .filter(produto=produto)
                        .aggregate(total=Sum('quantidade'))['total'] or 0
                    )
                else:
                    quantidade = Estoque_Produto.objects.get(
                        produto=produto,
                        deposito_id=deposito_id
                    ).quantidade

                resultado = "ok"

            except Produto.DoesNotExist:
                resultado = "nenhum_produto"
            except Estoque_Produto.DoesNotExist:
                resultado = "sem_estoque"

    return render(request, "estoque/verificacao/verificacao.html", {
        "depositos": depositos,
        "produto": produto,
        "quantidade": quantidade,
        "resultado": resultado,
        'historico': ultimas_acoes_modulo(request.user, 'estoque'),
    })


#DEPÓSITOS
@login_required
def depositos(request):

    # Total de depositos:
    total_depositos = Deposito.objects.count()

    search = request.GET.get("search")

    depositos = Deposito.objects.all()

    if search:
        depositos = depositos.filter(
            Q(descricao__icontains=search)
        )
    
    depositos = depositos.order_by('-id')

    paginator = Paginator(depositos, 10)
    numero_da_pagina = request.GET.get('p')
    depositos_paginados = paginator.get_page(numero_da_pagina)
    return render(request, "estoque/depositos/depositos.html", {"depositos": depositos_paginados, "search": search, "historico": ultimas_acoes_modulo(request.user, 'depositos'), "total_depositos": total_depositos})

@login_required
def adicionar_deposito(request):
    if request.method == "POST":
        form = DepositoForm(request.POST)
        if form.is_valid():
            depositos = form.save()

            messages.success(
                request,
                f"Depósito <strong>{depositos.descricao}</strong> adicionando com sucesso."
            )

            registrar_acao(
                request.user,
                'depositos',
                f"{depositos.descricao} adicionado"
            )
            return redirect("estoque:depositos")
    else:
        form = DepositoForm()
    return render(request, "estoque/depositos/adicionar_deposito.html", {"form": form, "historico": ultimas_acoes_modulo(request.user, 'depositos')})

@login_required
def editar_deposito(request, id_deposito):
    deposito = get_object_or_404(Deposito, id=id_deposito)

    if request.method == "POST":
        form = DepositoForm(request.POST, instance=deposito)
        if form.is_valid():
            deposito = form.save()
            messages.success(
                request,
                f"Depósito <strong>{deposito.descricao}</strong> editado com sucesso."
            )

            registrar_acao(
                request.user,
                'depositos',
                f"{deposito.nome} <strong>editado</strong>"
            )
            return redirect("estoque:depositos")
    else:
        form = DepositoForm(instance=deposito)

    return render(request, "estoque/depositos/editar_deposito.html", {"form": form, 'historico': ultimas_acoes_modulo(request.user, 'depositos'), "deposito": deposito})

@login_required
def excluir_deposito(request, id_deposito=0):
    if request.method == "POST":
        ids = request.POST.getlist("ids_selecionados")

        quantidade = len(ids)

        if quantidade > 0:
            Deposito.objects.filter(id__in=ids).delete() 
            messages.success(
                request,
                f"Depósito excluído com sucesso."
            )
            # REGISTRA A AÇÃO
            registrar_acao(
                usuario=request.user,
                modulo='depositos',
                descricao=f'{quantidade} deposito(s) excluído(s)'
            )
        return redirect('estoque:depositos')
    else:
        deposito = get_object_or_404(Deposito, id=id_deposito)
        return render(request, "estoque/depositos/confirma.html", {"deposito": deposito, "historico": ultimas_acoes_modulo(request.user, 'depositos')})

#PEDIDOS DE COMPRA
@login_required
def pedidos_compra(request):

    # Total de pedidos:
    total_pedidos = Pedidos_Compra.objects.filter(status__in=['aberto', 'processando']).count()

    search = request.GET.get("search")

    pedidos_compra = Pedidos_Compra.objects.filter(status__in=['aberto', 'processando'])

    if search:
        pedidos_compra = pedidos_compra.filter(
            Q(id__icontains=search) |
            Q(produto__nome__icontains=search) |
            Q(fornecedor__nome__icontains=search) |
            Q(id__icontains=search) 
        )
    
    pedidos_compra = pedidos_compra.order_by('-id')

    paginator = Paginator(pedidos_compra, 10)
    numero_da_pagina = request.GET.get('p')
    pedidos_compra_paginados = paginator.get_page(numero_da_pagina)
    return render(request, "estoque/pedidos_compra/pedidos_compra.html", {"pedidos_compra": pedidos_compra_paginados, "search": search, 'historico': ultimas_acoes_modulo(request.user, 'pedidos_compra'), "total_pedidos": total_pedidos})

@login_required
def adicionar_pedidos_compra(request):
    if request.method == "POST":
        form = Pedidos_CompraForm(request.POST)
        if form.is_valid():
            pedidos_compra = form.save()
            messages.success(
                request,
                f"Pedido de <strong>{pedidos_compra.produto.nome}</strong> cadastrado com sucesso."
            )

            registrar_acao(
                request.user,
                'pedidos_compra',
                f"Pedido de {pedidos_compra.produto.nome} cadastrado"
            )
            return redirect("estoque:pedidos_compra")
    else:
        form = Pedidos_CompraForm()
    return render(request, "estoque/pedidos_compra/adicionar_pedido_compra.html", {"form": form, 'historico': ultimas_acoes_modulo(request.user, 'pedidos_compra',)})

@login_required
def editar_pedido_compra(request, id_pedido):
    pedido_compra = get_object_or_404(Pedidos_Compra, id=id_pedido)

    if request.method == "POST":
        form = Pedidos_CompraForm(request.POST, instance=pedido_compra)
        if form.is_valid():
            pedidos_compra = form.save()
            messages.success(
                request,
                f"Pedido de {pedidos_compra.produto.nome} editado com sucesso."
            )

            registrar_acao(
                request.user,
                'pedidos_compra',
                f"Pedido de {pedidos_compra.produto.nome} <strong>editado</strong>"
            )
            return redirect("estoque:pedidos_compra")
    else:
        form = Pedidos_CompraForm(instance=pedido_compra)

    return render(request, "estoque/pedidos_compra/editar_pedido_compra.html", {"form": form, 'historico': ultimas_acoes_modulo(request.user, 'pedidos_compra'), "pedido_compra": pedido_compra})

@login_required
def excluir_pedido_compra(request, id_pedido=0):
    if request.method == "POST":
        ids = request.POST.getlist("ids_selecionados")

        quantidade = len(ids)

        if quantidade > 0:
            Pedidos_Compra.objects.filter(id__in=ids).delete() 
            messages.success(
                request,
                f"Pedido excluído com sucesso."
            )
            
            # REGISTRA A AÇÃO
            registrar_acao(
                usuario=request.user,
                modulo='pedidos_compra',
                descricao=f'{quantidade} pedido(s) excluído(s)'
            )
        return redirect('estoque:pedidos_compra')
    else:
        pedido = get_object_or_404(Pedidos_Compra, id=id_pedido)
        return render(request, "estoque/pedidos_compra/confirma.html", {"pedido": pedido, 'historico': ultimas_acoes_modulo(request.user, 'pedidos_compra'),})

#HISTÓRICO
@login_required
def historico_compra(request):

    # compras concluídas:
    total_compra = Pedidos_Compra.objects.filter(status='concluido').count()

    search = request.GET.get("search")

    pedidos = Pedidos_Compra.objects.filter(status__in=['concluido', 'cancelado'])

    if search:
        pedidos = pedidos.filter(
            Q(produto__nome__icontains=search) |
            Q(fornecedor__nome__icontains=search) 
        )

    pedidos = pedidos.order_by('-data')

    paginator = Paginator(pedidos, 10)
    numero_da_pagina = request.GET.get('p')
    pedidos_paginados = paginator.get_page(numero_da_pagina)
    return render(request, "estoque/pedidos_compra/historico.html", {"pedidos": pedidos_paginados, "search": search, "total_compra": total_compra})
