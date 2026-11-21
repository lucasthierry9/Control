from django.db import migrations


ESTADOS = [
    'AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
    'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN',
    'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO',
]


def popular_dados(apps, schema_editor):
    Estado = apps.get_model('control', 'Estado')
    for estado in ESTADOS:
        Estado.objects.get_or_create(estado=estado)

    Usuario = apps.get_model('usuarios', 'Usuario')
    empresa = Usuario.objects.filter(tipo='empresa').order_by('id').first()
    if empresa is None:
        empresa = Usuario.objects.order_by('id').first()

    if empresa:
        for model_name in (
            'Cliente', 'Fornecedor', 'Categoria_Produto', 'Produto',
            'Pedidos_Compra', 'Deposito', 'Movimentacao',
            'Vendedor', 'Pedidos_Venda',
        ):
            model = apps.get_model('control', model_name)
            model.objects.filter(empresa__isnull=True).update(empresa=empresa)

    PedidosVenda = apps.get_model('control', 'Pedidos_Venda')
    for pedido in PedidosVenda.objects.filter(preco_unitario__isnull=True).select_related('produto'):
        pedido.preco_unitario = pedido.produto.preco
        pedido.save(update_fields=['preco_unitario'])


def remover_dados(apps, schema_editor):
    Estado = apps.get_model('control', 'Estado')
    Estado.objects.filter(estado__in=ESTADOS).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('control', '0003_categoria_produto_empresa_cliente_empresa_and_more'),
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(popular_dados, remover_dados),
    ]
