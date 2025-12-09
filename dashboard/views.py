from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
    return render(request, 'dashboard/index.html' )
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