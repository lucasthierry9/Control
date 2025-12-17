from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, F, DecimalField, ExpressionWrapper
from django.db.models.functions import ExtractWeek, ExtractYear, ExtractMonth, ExtractDay, TruncMonth, Coalesce, TruncWeek
from datetime import datetime, timedelta
from django.utils import timezone
from control.models import Pedidos_Venda, Produto, Cliente, Pedidos_Compra, Estoque_Produto
import json
from django.utils.timezone import now
from decimal import Decimal

@login_required
def index(request):

    # CARDS
    total_produtos = Produto.objects.count()
    total_clientes = Cliente.objects.count()
    total_vendas = Pedidos_Venda.objects.filter(status__iexact='concluido').count()

    vendas_concluidas = Pedidos_Venda.objects.filter(status__iexact='concluido')

    faturamento = vendas_concluidas.aggregate(
        total=Sum(
            F('produto__preco') * F('quantidade'),
            output_field=DecimalField()
        )
    )['total'] or Decimal('0.00')

    # GRÁFICO: VENDAS ÚLTIMAS 4 SEMANAS 
    quatro_semanas_atras = timezone.now() - timedelta(weeks=4)

    vendas_semanais = (
        vendas_concluidas
        .filter(data__gte=quatro_semanas_atras)
        .annotate(semana=TruncWeek('data'))
        .values('semana')
        .annotate(total=Count('id'))
        .order_by('semana')
    )

    labels = []
    dados = []

    hoje = timezone.now().date()

    for i in range(3, -1, -1):
        inicio_semana = hoje - timedelta(days=hoje.weekday()) - timedelta(weeks=i)
        fim_semana = inicio_semana + timedelta(days=6)

        total = vendas_concluidas.filter(
            data__date__range=(inicio_semana, fim_semana)
        ).count()

        labels.append(inicio_semana.strftime('%d/%m'))
        dados.append(total)

    # GRÁFICO: FATURAMENTO MENSAL
    faturamento_mensal = (
        vendas_concluidas
        .annotate(mes=TruncMonth('data'))
        .values('mes')
        .annotate(
            total=Sum(
                F('produto__preco') * F('quantidade'),
                output_field=DecimalField()
            )
        )
        .order_by('mes')
    )

    labels_faturamento = []
    dados_faturamento = []

    for f in faturamento_mensal:
        labels_faturamento.append(f['mes'].strftime('%b/%Y'))
        dados_faturamento.append(float(f['total'] or 0))

    # Limita aos últimos 12 meses
    labels_faturamento = labels_faturamento[-12:]
    dados_faturamento = dados_faturamento[-12:]

    return render(request, 'dashboard/index.html', {
        # Cards
        'total_produtos': total_produtos,
        'total_clientes': total_clientes,
        'total_vendas': total_vendas,
        'faturamento': faturamento,

        # Gráfico vendas
        'labels_json': json.dumps(labels),
        'vendas_json': json.dumps(dados),

        # Gráfico faturamento
        'labels_faturamento_json': json.dumps(labels_faturamento),
        'faturamento_json': json.dumps(dados_faturamento),
    })


@login_required
def vendas(request):
    # Vendas concluídas:
    total_vendas = Pedidos_Venda.objects.filter(status='concluido').count()

    # Vendedor com mais vendas realizadas
    vendedor_vendas = Pedidos_Venda.objects.filter(status='concluido').values('vendedor__id', 'vendedor__nome' ).annotate(total_quantidade=Sum('quantidade')).order_by('-total_quantidade')
    
    # Valores padrão
    nome_vendedor = "Nenhum"
    quantidade_vendedor = 0

    vendedor_mais_vendas = vendedor_vendas.first()
    if vendedor_mais_vendas:
        nome_vendedor = vendedor_mais_vendas['vendedor__nome']
        quantidade_vendedor = vendedor_mais_vendas['total_quantidade']

    # Valor mais alto em uma venda
    maior_venda = Pedidos_Venda.objects.filter(status='concluido').annotate(valor_total=ExpressionWrapper(F('produto__preco') * F('quantidade'),
        output_field=DecimalField(max_digits=10, decimal_places=2))).order_by('-valor_total').first()
    
    if maior_venda:
        maior_valor_venda = maior_venda.valor_total
    else:
        maior_valor_venda = 0


    # Gráfico status de vendas
    status_map = {
        'concluido': {
            'label': 'Concluído',
            'color': '#22c55e'
        },
        'aberto': {
            'label': 'Aberto',
            'color': '#3b82f6'
        },
        'processando': {
            'label': 'Processando',
            'color': '#fb923c'
        },
        'cancelado': {
            'label': 'Cancelado',
            'color': '#ef4444'
        },
    }
    
    status_vendas = (
        Pedidos_Venda.objects
        .values('status')
        .annotate(total=Count('id'))
    )

    labels_status = []
    dados_status = []
    cores_status = []

    for s in status_vendas:
        status_key = s['status'].lower()
        if status_key in status_map:
            labels_status.append(status_map[status_key]['label'])
            dados_status.append(s['total'])
            cores_status.append(status_map[status_key]['color'])

    # Gráfico linha vendas mensais
    ano = request.GET.get('ano')

    vendas_mensais_qs = Pedidos_Venda.objects.filter(status='concluido')

    # Se tiver filtro de ano, usa ele
    if ano:
        vendas_mensais_qs = vendas_mensais_qs.filter(data__year=int(ano))
    else:
        # Se NÃO tiver ano, pega últimos 12 meses
        data_inicio = now().date().replace(day=1) - timedelta(days=365)
        vendas_mensais_qs = vendas_mensais_qs.filter(data__date__gte=data_inicio)

    vendas_mensais = (
        vendas_mensais_qs
        .annotate(mes=TruncMonth('data'))
        .values('mes')
        .annotate(total=Count('id'))
        .order_by('mes')
    )

    labels_mensal = []
    dados_mensal = []

    for v in vendas_mensais:
        labels_mensal.append(v['mes'].strftime('%b/%Y'))
        dados_mensal.append(v['total'])

    return render(request, 'dashboard/vendas.html', {
    # Vendas concluídas:
    "total_vendas": total_vendas, 

    #Vendedor com mais vendas:
    "vendedor": nome_vendedor, 
    "quantidade_vendedor": quantidade_vendedor,

    # Maior valor em uma venda
    "maior_valor_venda": maior_valor_venda,
    
    # Gráfico status vendas: 
    "labels_status_json": json.dumps(labels_status),
    "dados_status_json": json.dumps(dados_status),
    "cores_status_json": json.dumps(cores_status),
    
    # Gráfico linha vendas mensais:
    "labels_mensal_json": json.dumps(labels_mensal),
    "dados_mensal_json": json.dumps(dados_mensal),})


@login_required
def produtos(request):

    total_produtos = Produto.objects.count()

    # Obter filtros
    ano = request.GET.get('ano')
    mes = request.GET.get('mes')

    # Porcentagem de clientes que não realizaram nenhum pedido
    # Clientes que possuem ao menos 1 pedido
    produtos_com_pedido = (
        Produto.objects.filter(pedidos_venda__status='concluido')
        .annotate(total_pedidos=Count('pedidos_venda'))
        .filter(total_pedidos__gt=0)
        .count()
    )

    produtos_sem_pedido = total_produtos - produtos_com_pedido

    percentual_sem_pedido = 0
    if total_produtos > 0:
        percentual_sem_pedido = round(
            (produtos_sem_pedido / total_produtos) * 100, 2
        )

    produtos_sem_estoque = (
        Produto.objects
        .annotate(
            total_estoque=Coalesce(
                Sum('estoque_produto__quantidade'),
                0
            )
        )
        .filter(total_estoque__lte=0)
        .count()
    )

    # TOP 5 PRODUTOS MAIS VENDIDOS
    produtos_mais_vendidos = (
        Pedidos_Venda.objects
        .filter(status='concluido')
        .values('produto__nome')
        .annotate(total_vendido=Sum('quantidade'))
        .order_by('-total_vendido')[:5]
    )

    labels_produtos = []
    dados_produtos = []

    for p in produtos_mais_vendidos:
        labels_produtos.append(p['produto__nome'])
        dados_produtos.append(p['total_vendido'])

    # Produtos maior faturamento
    produtos_faturamento = (
        Pedidos_Venda.objects
        .filter(status='concluido')
        .values('produto__nome')
        .annotate(
            faturamento=Sum(
                F('produto__preco') * F('quantidade'),
                output_field=DecimalField()
            )
        )
        .order_by('-faturamento')[:5]  # TOP 5
    )

    labels_produtos_faturamento = []
    dados_produtos_faturamento = []

    for p in produtos_faturamento:
        labels_produtos_faturamento.append(p['produto__nome'])
        dados_produtos_faturamento.append(float(p['faturamento']))

    return render(request, 'dashboard/produtos.html', {
        "total_produtos": total_produtos,
        "produtos_sem_estoque": produtos_sem_estoque,
        
        "labels_produtos_json": json.dumps(labels_produtos),
        "dados_produtos_json": json.dumps(dados_produtos),
        
        'labels_produtos_faturamento_json': json.dumps(labels_produtos_faturamento),
        'dados_produtos_faturamento_json': json.dumps(dados_produtos_faturamento),
        
        # PORCENTAGEM DE CLIENTES QUE NÃO REALIZARAM PEDIDOS
        'produtos_sem_pedido': produtos_sem_pedido,
        'percentual_sem_pedido': percentual_sem_pedido,})



@login_required
def clientes(request):

    # Total de clientes cadastrados
    total_clientes = Cliente.objects.count()

    # Cliente com mais pedidos
    cliente_mais_pedidos = (
        Pedidos_Venda.objects
        .values('cliente__id', 'cliente__nome')
        .annotate(total_pedidos=Count('id'))
        .order_by('-total_pedidos')
        .first()
    )

    if cliente_mais_pedidos:
        nome_cliente_mais_pedidos = cliente_mais_pedidos['cliente__nome']
    else:
        nome_cliente_mais_pedidos = 'Nenhum'

    # Porcentagem de clientes que não realizaram nenhum pedido
    # Clientes que possuem ao menos 1 pedido
    clientes_com_pedido = (
        Cliente.objects.filter(pedidos_venda__status='concluido')
        .annotate(total_pedidos=Count('pedidos_venda'))
        .filter(total_pedidos__gt=0)
        .count()
    )

    clientes_sem_pedido = total_clientes - clientes_com_pedido

    percentual_sem_pedido = 0
    if total_clientes > 0:
        percentual_sem_pedido = round(
            (clientes_sem_pedido / total_clientes) * 100, 2
        )

    # CLIENTES CADASTRADOS POR SEMANA GRÁFICO
    hoje = now().date()
    quatro_semanas_atras = hoje - timedelta(weeks=4)

    clientes = Cliente.objects.filter(
        data_cadastro__date__gte=quatro_semanas_atras
    )

    clientes_semana = (
        clientes
        .annotate(semana=ExtractWeek('data_cadastro'))
        .values('semana')
        .annotate(total=Count('id'))
        .order_by('semana')
    )

    labels_clientes = []
    dados_clientes = []

    for i, c in enumerate(clientes_semana, start=1):
        labels_clientes.append(f"Semana {i}")
        dados_clientes.append(c['total'])

    # TOP 5 CLIENTES COM MAIS PEDIDOS GRÁFICO
    top_clientes = (
        Pedidos_Venda.objects
        .filter(status='concluido')
        .values('cliente__nome')
        .annotate(total_pedidos=Count('id'))
        .order_by('-total_pedidos')[:5]
    )

    labels_top_clientes = [c['cliente__nome'] for c in top_clientes]
    dados_top_clientes = [c['total_pedidos'] for c in top_clientes]

    return render(request, 'dashboard/clientes.html', {
        # CLIENTES CADASTRADOS POR SEMANA GRÁFICO
        'labels_clientes_json': json.dumps(labels_clientes),
        'dados_clientes_json': json.dumps(dados_clientes),

        # TOP 5 CLIENTES COM MAIS PEDIDOS GRÁFICO
        'labels_top_clientes_json': json.dumps(labels_top_clientes),
        'dados_top_clientes_json': json.dumps(dados_top_clientes),

        # TOTAL DE CLIENTES CADASTRADOS
        "total_clientes": total_clientes,

        # CLIENTE COM MAIS PEDIDOS
        'cliente_mais_pedidos': nome_cliente_mais_pedidos,

        # PORCENTAGEM DE CLIENTES QUE NÃO REALIZARAM PEDIDOS
        'clientes_sem_pedido': clientes_sem_pedido,
        'percentual_sem_pedido': percentual_sem_pedido,
    } )







@login_required
def charts(request):
    return render(request, 'dashboard/charts.html' )

@login_required
def tables(request):
    return render(request, 'dashboard/tables.html' )