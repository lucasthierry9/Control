from django.urls import path
from . import views
app_name = 'cadastros'
urlpatterns = [
    path("cadastrar-cliente/", views.cadastrar_cliente, name="cadastrar_cliente"),
    path("clientes/", views.clientes, name="clientes"),
    path("editar-cliente/<int:id_cliente>/", views.editar_cliente, name="editar_cliente"),
    path("excluir-cliente/<int:id_cliente>/", views.excluir_cliente, name="excluir_cliente"),
    path("produtos/", views.produtos, name="produtos"),
    path("cadastrar-produto/", views.cadastrar_produto, name="cadastrar_produto"),
    path("editar-produto/<int:id_produto>/", views.editar_produto, name="editar_produto"),
    path("excluir-produto/<int:id_produto>/", views.excluir_produto, name="excluir_produto"),
    path("funcionarios/", views.funcionarios, name="funcionarios"),
    path("cadastrar-funcionario/", views.cadastrar_funcionario, name="cadastrar_funcionario"),
    path("editar-funcionario/<int:id_funcionario>/", views.editar_funcionario, name="editar_funcionario"),
    path("excluir-funcionario/<int:id_funcionario>/", views.excluir_funcionario, name="excluir_funcionario"),
]