from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
    return render(request, 'dashboard/index.html' )
def charts(request):
    return render(request, 'dashboard/charts.html' )
def tables(request):
    return render(request, 'dashboard/tables.html' )
def vendas(request):
    return render(request, 'dashboard/vendas.html' )
def clientes(request):
    return render(request, 'dashboard/clientes.html' )
def produtos(request):
    return render(request, 'dashboard/produtos.html' )