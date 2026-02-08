from django.urls import path
from . import views
app_name = 'estoque'
urlpatterns = [
    path("movimentacoes/", views.movimentacoes, name="movimentacoes"),
    path("adicionar-movimentacao/", views.adicionar_movimentacao, name="adicionar_movimentacao"),
    path("editar-movimentacao/<int:id_movimentacao>", views.editar_movimentacao, name="editar_movimentacao"),
    path("excluir-movimentacao/", views.excluir_movimentacao, name="excluir_movimentacao"),

    path("verficacao/", views.verificacao, name="verificacao"),

    path("depositos/", views.depositos, name="depositos"),
    path("adicionar-deposito/", views.adicionar_deposito, name="adicionar_deposito"),
    path("editar-deposito/<int:id_deposito>", views.editar_deposito, name="editar_deposito"),
    path("excluir-deposito/", views.excluir_deposito, name="excluir_deposito"),

    path("pedidos-compra/", views.pedidos_compra, name="pedidos_compra"),
    path("adicionar-pedido-compra/", views.adicionar_pedidos_compra, name="adicionar_pedido_compra"),
    path("editar-pedido-compra/<int:id_pedido>/", views.editar_pedido_compra, name="editar_pedido_compra"),
    path("excluir-pedido-compra/", views.excluir_pedido_compra, name="excluir_pedido_compra"),
    path("historico_compra/", views.historico_compra, name="historico_compra"),
]