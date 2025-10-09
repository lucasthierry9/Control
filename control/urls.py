from django.urls import path
from . import views
urlpatterns = [
    path('',views.index, name="index"),
    path('login/', views.login, name="login"),
    path("cadastrar_cliente/", views.cadastrar_cliente, name="cadastrar_cliente"),
    path("clientes/", views.clientes, name="clientes"),
    path("editar_cliente/<int:id_cliente>/", views.editar_cliente, name="editar_cliente"),
    path("excluir_cliente/<int:id_cliente>/", views.excluir_cliente, name="excluir_cliente"),
]
