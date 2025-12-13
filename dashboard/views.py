from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum # Usamos Count para contar os pedidos
from django.db.models.functions import ExtractWeek, ExtractYear, ExtractMonth, ExtractDay
from datetime import datetime, timedelta
from django.utils import timezone
from control.models import Pedidos_Venda
import json
from django.utils.timezone import now

@login_required
def index(request):
    ano = request.GET.get('ano')
    mes = request.GET.get('mes')

    vendas = Pedidos_Venda.objects.filter(status__iexact='concluido')

    if ano:
        vendas = vendas.filter(data__year=int(ano))

    # ==================================================
    # 🔥 CASO 1 — TEM MÊS → SEMANA 1,2,3,4 DO MÊS
    # ==================================================
    if mes:
        vendas = vendas.filter(data__month=int(mes))

        vendas_por_dia = (
            vendas
            .annotate(dia=ExtractDay('data'))
            .values('dia')
            .annotate(total=Count('id'))
        )

        semanas = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

        for v in vendas_por_dia:
            dia = v['dia']
            semana_do_mes = (dia - 1) // 7 + 1
            semanas[semana_do_mes] += v['total']

        labels = [f"Semana {s}" for s in semanas if semanas[s] > 0]
        dados = [semanas[s] for s in semanas if semanas[s] > 0]

    # ==================================================
    # 🔥 CASO 2 — SEM MÊS → ÚLTIMAS 4 SEMANAS
    # ==================================================
    else:
        hoje = now().date()
        quatro_semanas_atras = hoje - timedelta(weeks=4)

        vendas = vendas.filter(data__date__gte=quatro_semanas_atras)

        vendas_semana = (
            vendas
            .annotate(semana=ExtractWeek('data'))
            .values('semana')
            .annotate(total=Count('id'))
            .order_by('semana')
        )

        labels = []
        dados = []

        for i, v in enumerate(vendas_semana, start=1):
            labels.append(f"Semana {i}")
            dados.append(v['total'])

    # ==================================================
    # 🔹 FILTROS
    # ==================================================
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
        'anos': anos,
        'meses': meses,
        'ano_selecionado': ano,
        'mes_selecionado': int(mes) if mes else '',
    })

@login_required
def charts(request):
    return render(request, 'dashboard/charts.html' )
@login_required
def tables(request):
    return render(request, 'dashboard/tables.html' )
@login_required
def vendas(request):
    return render(request, 'dashboard/vendas.html' )
@login_required
def clientes(request):
    return render(request, 'dashboard/clientes.html' )
@login_required
def produtos(request):
    return render(request, 'dashboard/produtos.html' )