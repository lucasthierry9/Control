from django.urls import path
from . import views
app_name = 'vendas'
urlpatterns = [
    path("registrar-pedido/", views.registrar_pedido, name="registrar_pedido"),
    path("pedidos/", views.pedidos, name="pedidos"),
    path("editar-pedido/<int:id_pedido>/", views.editar_pedido, name="editar_pedido"),
    path("excluir-pedido/<int:id_pedido>/", views.excluir_pedido, name="excluir_pedido"),

    path("historico/", views.historico, name="historico"),

    path("relatorio-vendas/", views.relatorio_vendas, name="relatorio_vendas"),
]