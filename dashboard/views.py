from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Count, Sum # Usamos Count para contar os pedidos
from django.db.models.functions import TruncWeek, TruncMonth # TruncWeek é a chave
from datetime import datetime, timedelta
from django.utils import timezone
from control.models import Pedidos_Venda

@login_required
def index(request):
    context = {
        "labels": 1,
        "data": [5, 10, 15, 20],
    }

    return render(request, 'dashboard/index.html', context)

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