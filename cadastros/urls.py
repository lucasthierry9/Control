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

    path("vendedores/", views.vendedores, name="vendedores"),
    path("cadastrar-vendedor/", views.cadastrar_vendedor, name="cadastrar_vendedor"),
    path("editar-vendedor/<int:id_vendedor>/", views.editar_vendedor, name="editar_vendedor"),
    path("excluir-vendedor/<int:id_vendedor>/", views.excluir_vendedor, name="excluir_vendedor"),

    path("fornecedores/", views.fornecedores, name="fornecedores"),
    path("cadastrar-fornecedor/", views.cadastrar_fornecedor, name="cadastrar_fornecedor"),
    path("editar-fornecedor/<int:id_fornecedor>/", views.editar_fornecedor, name="editar_fornecedor"),
    path("excluir-fornecedor/<int:id_fornecedor>/", views.excluir_fornecedor, name="excluir_fornecedor"),

    path("categorias/", views.categorias, name="categorias"),
    path("cadastrar-categoria/", views.cadastrar_categoria, name="cadastrar_categoria"),
    path("editar-categoria/<int:id_categoria>/", views.editar_categoria, name="editar_categoria"),
    path("excluir-categoria/<int:id_categoria>/", views.excluir_categoria, name="excluir_categoria"),
]