from django.urls import path
from . import views
app_name = 'dashboard'
urlpatterns = [
    path("", views.index, name='index'),
    path("tables/", views.tables, name='tables'),
    path("clientes/", views.clientes, name='clientes'),
    path("vendas/", views.vendas, name='vendas'),
    path("charts/", views.charts, name='charts'),
    path("produtos/", views.produtos, name='produtos'),

]
