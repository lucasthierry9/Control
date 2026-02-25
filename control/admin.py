from django.contrib import admin
from . models import *
from usuarios.models import Usuario

admin.site.register(Usuario)
admin.site.register(Estado)
admin.site.register(Cidade)
admin.site.register(Bairro)
admin.site.register(Fornecedor)
admin.site.register(Cliente)
admin.site.register(Categoria_Produto)
admin.site.register(Produto)
admin.site.register(Funcionario)
admin.site.register(Vendedor)