from django.urls import path
from . import views
app_name = 'estoque'
urlpatterns = [
    path("movimentacoes/", views.movimentacoes, name="movimentacoes"),
    path("adicionar-movimentacao/", views.adicionar_movimentacao, name="adicionar_movimentacao"),

    path("verficacao/", views.verificacao, name="verificacao"),

    path("depositos/", views.depositos, name="depositos"),
    path("adicionar-deposito/", views.adicionar_deposito, name="adicionar_deposito"),
    path("excluir-deposito/", views.excluir_deposito, name="excluir_deposito"),

    path("pedidos-compra/", views.pedidos_compra, name="pedidos_compra"),
    path("adicionar-pedido-compra/", views.adicionar_pedidos_compra, name="adicionar_pedido_compra"), 
]