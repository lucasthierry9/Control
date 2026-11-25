from datetime import datetime, time, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from control.models import (
    Categoria_Produto,
    Cliente,
    Deposito,
    Estado,
    Fornecedor,
    Movimentacao,
    Pedidos_Compra,
    Pedidos_Venda,
    Produto,
    Vendedor,
)
from control.utils import empresa_do_usuario


class Command(BaseCommand):
    help = "Carrega dados fictícios de demonstração para uma empresa existente."

    def add_arguments(self, parser):
        parser.add_argument(
            "--email",
            required=True,
            help="E-mail da conta da empresa ou do funcionário que fará o teste.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        User = get_user_model()
        try:
            usuario = User.objects.get(email=options["email"])
        except User.DoesNotExist as exc:
            raise CommandError(
                f"Não existe uma conta cadastrada com o e-mail {options['email']}."
            ) from exc

        empresa = empresa_do_usuario(usuario)
        if empresa is None:
            raise CommandError(
                "A conta de funcionário não está vinculada a uma empresa."
            )

        estado, _ = Estado.objects.get_or_create(estado="RN")
        categoria_papelaria, _ = Categoria_Produto.objects.get_or_create(
            empresa=empresa,
            nome="Demo - Papelaria",
            defaults={"descricao": "Materiais de escritório para demonstração"},
        )
        categoria_informatica, _ = Categoria_Produto.objects.get_or_create(
            empresa=empresa,
            nome="Demo - Informática",
            defaults={"descricao": "Acessórios de informática para demonstração"},
        )
        categoria_alimentos, _ = Categoria_Produto.objects.get_or_create(
            empresa=empresa,
            nome="Demo - Alimentos",
            defaults={"descricao": "Produtos alimentícios para demonstração"},
        )

        products_data = [
            (categoria_papelaria, "Demo - Caderno", "24.90"),
            (categoria_informatica, "Demo - Mouse sem fio", "59.90"),
            (categoria_alimentos, "Demo - Café especial", "32.50"),
            (categoria_papelaria, "Demo - Canetas (kit)", "14.00"),
            (categoria_informatica, "Demo - Teclado compacto", "129.90"),
            (categoria_alimentos, "Demo - Biscoitos artesanais", "18.75"),
        ]
        products = []
        for categoria, nome, preco in products_data:
            produto, _ = Produto.objects.get_or_create(
                empresa=empresa,
                nome=nome,
                defaults={
                    "categoria": categoria,
                    "preco": preco,
                },
            )
            products.append(produto)

        clients_data = [
            ("Cliente Demo - Ana Lima", "90000000001"),
            ("Cliente Demo - Bruno Reis", "90000000002"),
            ("Cliente Demo - Caio Nunes", "90000000003"),
            ("Cliente Demo - Dora Alves", "90000000004"),
            ("Cliente Demo - Enzo Costa", "90000000005"),
        ]
        clients = []
        for nome, cpf in clients_data:
            cliente, _ = Cliente.objects.get_or_create(
                empresa=empresa,
                nome=nome,
                defaults={
                    "cpf": cpf,
                    "email": f"{cpf[-2:]}@clientes.exemplo.com",
                    "telefone": f"8499000{cpf[-4:]}",
                    "estado": estado,
                    "cidade": "Natal",
                    "bairro": "Centro",
                    "logradouro": "Rua de Demonstração",
                    "numero": cpf[-2:],
                    "cep": "59000000",
                },
            )
            clients.append(cliente)

        suppliers_data = [
            ("Fornecedor Demo - Atacado Potiguar", "00000000000101"),
            ("Fornecedor Demo - Comercial Exemplo", "00000000000102"),
        ]
        suppliers = []
        for nome, cnpj in suppliers_data:
            fornecedor, _ = Fornecedor.objects.get_or_create(
                empresa=empresa,
                nome=nome,
                defaults={
                    "cpf_cnpj": cnpj,
                    "email": f"{cnpj[-2:]}@fornecedores.exemplo.com",
                    "telefone": f"8430000{cnpj[-4:]}",
                    "estado": estado,
                    "cidade": "Natal",
                    "bairro": "Centro",
                    "logradouro": "Avenida de Demonstração",
                    "numero": cnpj[-2:],
                    "cep": "59000000",
                },
            )
            suppliers.append(fornecedor)

        sellers_data = [
            ("Vendedor Demo - Marina", "80000000001"),
            ("Vendedor Demo - Rafael", "80000000002"),
        ]
        sellers = []
        for nome, cpf in sellers_data:
            vendedor, _ = Vendedor.objects.get_or_create(
                empresa=empresa,
                nome=nome,
                defaults={
                    "cpf": cpf,
                    "email": f"{cpf[-2:]}@vendedores.exemplo.com",
                    "telefone": f"8498000{cpf[-4:]}",
                },
            )
            sellers.append(vendedor)

        deposito, _ = Deposito.objects.get_or_create(
            empresa=empresa,
            descricao="Demo - Estoque principal",
        )
        hoje = timezone.localdate()
        fuso = timezone.get_current_timezone()

        def data_dias_atras(dias, hora=10):
            data = datetime.combine(hoje - timedelta(days=dias), time(hour=hora))
            return timezone.make_aware(data, fuso)

        # Entradas iniciais variadas também deixam exemplos de estoque baixo e zerado.
        for produto, quantidade in zip(products, (80, 50, 35, 20, 4, 3)):
            Movimentacao.objects.get_or_create(
                empresa=empresa,
                deposito=deposito,
                produto=produto,
                tipo="entrada",
                defaults={
                    "dataehora": data_dias_atras(180),
                    "quantidade": quantidade,
                    "preco_custo": produto.preco,
                    "preco_compra": produto.preco,
                },
            )
        Movimentacao.objects.get_or_create(
            empresa=empresa,
            deposito=deposito,
            produto=products[5],
            tipo="saida",
            defaults={
                "dataehora": data_dias_atras(179),
                "quantidade": 3,
                "preco_custo": products[5].preco,
                "preco_compra": None,
            },
        )

        purchases_data = [
            (products[0], suppliers[0], 24, "598.00", "concluido", 20),
            (products[1], suppliers[1], 12, "718.80", "aberto", 8),
            (products[2], suppliers[0], 18, "585.00", "processando", 4),
        ]
        for produto, fornecedor, quantidade, valor, status, dias in purchases_data:
            Pedidos_Compra.objects.update_or_create(
                empresa=empresa,
                produto=produto,
                fornecedor=fornecedor,
                defaults={
                    "data": data_dias_atras(dias, 9),
                    "deposito": deposito,
                    "quantidade": quantidade,
                    "valor": valor,
                    "status": status,
                },
            )

        sales_data = [
            (0, 0, 0, 2, "concluido", 2),
            (1, 1, 1, 1, "concluido", 6),
            (2, 2, 0, 3, "concluido", 9),
            (3, 3, 1, 2, "concluido", 13),
            (0, 4, 0, 1, "concluido", 16),
            (1, 0, 1, 2, "concluido", 20),
            (2, 1, 0, 1, "concluido", 26),
            (3, 2, 1, 2, "concluido", 34),
            (4, 3, 0, 1, "concluido", 62),
            (4, 4, 1, 1, "aberto", 95),
            (0, 2, 0, 2, "processando", 126),
            (1, 3, 1, 1, "cancelado", 158),
        ]
        for indice, (cliente_idx, produto_idx, vendedor_idx, quantidade, status, dias) in enumerate(
            sales_data
        ):
            Pedidos_Venda.objects.update_or_create(
                empresa=empresa,
                cliente=clients[cliente_idx],
                produto=products[produto_idx],
                defaults={
                    "data": data_dias_atras(dias, 11 + indice % 6),
                    "vendedor": sellers[vendedor_idx],
                    "quantidade": quantidade,
                    "pagamento": ("pix", "credito", "debito", "dinheiro")[indice % 4],
                    "status": status,
                    "frete": ("cif", "fob", "retirar")[indice % 3],
                    "valor_frete": "12.00" if indice % 3 != 2 else "0.00",
                    "estado": estado,
                    "cidade": "Natal",
                    "bairro": "Centro",
                    "logradouro": "Rua de Demonstração",
                    "numero": str(indice + 1),
                    "cep": "59000000",
                    "preco_unitario": products[produto_idx].preco,
                },
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Dados de demonstração carregados para {empresa.email}. "
                f"{len(products)} produtos, {len(clients)} clientes e "
                f"{len(sales_data)} vendas disponíveis."
            )
        )
