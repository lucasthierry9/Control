from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, F, DecimalField, ExpressionWrapper
from django.db.models.functions import ExtractWeek, ExtractYear, ExtractMonth, ExtractDay, TruncMonth
from datetime import datetime, timedelta
from django.utils import timezone
from control.models import Pedidos_Venda, Produto, Cliente, Pedidos_Compra
import json
from django.utils.timezone import now
from decimal import Decimal

@login_required
def index(request):
    # Totais básicos (não filtrados por data)
    total_produtos = Produto.objects.count()
    total_clientes = Cliente.objects.count()
    total_vendas = Pedidos_Venda.objects.filter(status='concluido').count()
    
    # Obter filtros
    ano = request.GET.get('ano')
    mes = request.GET.get('mes')
    
    # Query comum para vendas concluídas
    vendas_concluidas = Pedidos_Venda.objects.filter(status__iexact='concluido')
    compras_concluidas = Pedidos_Compra.objects.filter(status__iexact='concluido')
    
    # Aplicar filtros de data
    if ano:
        ano_int = int(ano)
        vendas_concluidas = vendas_concluidas.filter(data__year=ano_int)
        compras_concluidas = compras_concluidas.filter(data__year=ano_int)
    
    if mes:
        mes_int = int(mes)
        vendas_concluidas = vendas_concluidas.filter(data__month=mes_int)
        compras_concluidas = compras_concluidas.filter(data__month=mes_int)
    
    # Cálculo do faturamento
    valor_total_vendas = vendas_concluidas.aggregate(
        total=Sum(F('produto__preco') * F('quantidade'), output_field=DecimalField())
    )['total'] or Decimal('0.00')
    
    valor_total_compras = compras_concluidas.aggregate(
        total=Sum('valor', output_field=DecimalField())
    )['total'] or Decimal('0.00')
    
    faturamento = valor_total_vendas - valor_total_compras
    
    # Gráfico de vendas por semana/dia
    vendas_para_grafico = vendas_concluidas  # Já está filtrado
    
    if mes:
        # Vendas por semana do mês
        vendas_por_dia = (
            vendas_para_grafico
            .annotate(dia=ExtractDay('data'))
            .values('dia')
            .annotate(total=Count('id'))
        )
        
        # Inicializar semanas
        semanas = {i: 0 for i in range(1, 6)}  # Semanas 1-5
        
        for v in vendas_por_dia:
            dia = v['dia']
            semana_do_mes = (dia - 1) // 7 + 1
            if semana_do_mes in semanas:
                semanas[semana_do_mes] += v['total']
        
        # Filtrar semanas com vendas
        semanas_com_vendas = {k: v for k, v in semanas.items() if v > 0}
        labels = [f"Semana {s}" for s in semanas_com_vendas.keys()]
        dados = list(semanas_com_vendas.values())
        
    else:
        # Vendas das últimas 4 semanas
        quatro_semanas_atras = timezone.now() - timedelta(weeks=4)
        vendas_ultimas_4_semanas = vendas_para_grafico.filter(data__gte=quatro_semanas_atras)
        
        vendas_semana = (
            vendas_ultimas_4_semanas
            .annotate(semana=ExtractWeek('data'))
            .values('semana')
            .annotate(total=Count('id'))
            .order_by('semana')
        )
        
        # Garantir 4 semanas mesmo sem dados
        labels = []
        dados = []
        
        semanas_dict = {v['semana']: v['total'] for v in vendas_semana}
        
        for i in range(1, 5):
            labels.append(f"Semana {i}")
            semana_num = (timezone.now() - timedelta(weeks=4-i)).isocalendar()[1]
            dados.append(semanas_dict.get(semana_num, 0))
    
    # Gráfico de faturamento mensal
    vendas_mensal = (
        Pedidos_Venda.objects
        .filter(status='concluido')
        .annotate(mes=TruncMonth('data'))
        .values('mes')
        .annotate(
            valor_total=Sum(
                F('produto__preco') * F('quantidade'),
                output_field=DecimalField()
            )
        )
        .order_by('mes')
    )
    
    compras_mensal = (
        Pedidos_Compra.objects
        .filter(status='concluido')
        .annotate(mes=TruncMonth('data'))
        .values('mes')
        .annotate(total_compras=Sum('valor'))
        .order_by('mes')
    )
    
    # Converter para dicionários para fácil acesso
    compras_dict = {c['mes']: c['total_compras'] or Decimal('0.00') for c in compras_mensal}
    
    # Preparar dados para o gráfico
    labels_faturamento = []
    dados_faturamento = []
    
    for v in vendas_mensal:
        mes_ref = v['mes']
        valor_vendas = v['valor_total'] or Decimal('0.00')
        valor_compras = compras_dict.get(mes_ref, Decimal('0.00'))
        faturamento_mensal = valor_vendas - valor_compras
        
        labels_faturamento.append(mes_ref.strftime('%b/%Y'))
        dados_faturamento.append(float(faturamento_mensal))
    
    # Filtrar para mostrar apenas últimos 12 meses
    if len(labels_faturamento) > 12:
        labels_faturamento = labels_faturamento[-12:]
        dados_faturamento = dados_faturamento[-12:]
    
    # Listas para filtros
    anos = (
        Pedidos_Venda.objects
        .annotate(ano=ExtractYear('data'))
        .values_list('ano', flat=True)
        .distinct()
        .order_by('-ano')
    )
    
    meses = [
        (1, 'Janeiro'), (2, 'Fevereiro'), (3, 'Março'),
        (4, 'Abril'), (5, 'Maio'), (6, 'Junho'),
        (7, 'Julho'), (8, 'Agosto'), (9, 'Setembro'),
        (10, 'Outubro'), (11, 'Novembro'), (12, 'Dezembro'),
    ]
    
    return render(request, 'dashboard/index.html', {
        'labels_json': json.dumps(labels),
        'vendas_json': json.dumps(dados),
        'labels_faturamento_json': json.dumps(labels_faturamento),
        'faturamento_json': json.dumps(dados_faturamento),
        'anos': anos,
        'meses': meses,
        'ano_selecionado': ano,
        'mes_selecionado': int(mes) if mes else None,
        'total_produtos': total_produtos,
        'total_clientes': total_clientes,
        'total_vendas': total_vendas,
        'valor_total_vendas': valor_total_vendas,  # Já calculado acima
        'faturamento': faturamento  # Já calculado acima
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
def clientes(request):
    return render(request, 'dashboard/clientes.html' )

@login_required
def produtos(request):
    return render(request, 'dashboard/produtos.html' )





@login_required
def charts(request):
    return render(request, 'dashboard/charts.html' )

@login_required
def tables(request):
    return render(request, 'dashboard/tables.html' )