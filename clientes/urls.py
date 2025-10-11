from django.urls import path
from . import views
app_name = 'clientes'
urlpatterns = [
    path("cadastrar-cliente/", views.cadastrar_cliente, name="cadastrar_cliente"),
    path("", views.clientes, name="clientes"),
    path("editar-cliente/<int:id_cliente>/", views.editar_cliente, name="editar_cliente"),
    path("excluir-cliente/<int:id_cliente>/", views.excluir_cliente, name="excluir_cliente"),
    
]