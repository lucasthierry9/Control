from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from control.forms import FornecedorForm
from control.models import Cliente, Fornecedor, Pedidos_Venda, Produto


class FornecedorFormTests(TestCase):
    def test_only_supplier_name_is_required(self):
        form = FornecedorForm(data={"nome": "Fornecedor rápido"})

        self.assertTrue(form.is_valid(), form.errors)
        fornecedor = form.save()

        self.assertEqual(fornecedor.nome, "Fornecedor rápido")
        self.assertEqual(fornecedor.cpf_cnpj, "")
        self.assertEqual(fornecedor.email, "")
        self.assertEqual(fornecedor.telefone, "")

    def test_supplier_name_remains_required(self):
        form = FornecedorForm(data={})

        self.assertFalse(form.is_valid())
        self.assertIn("nome", form.errors)


class LoadDemoDataCommandTests(TestCase):
    def setUp(self):
        self.empresa = get_user_model().objects.create_user(
            email="demo.empresa@example.com",
            password="senha-de-teste",
            razao_social="Empresa de Demonstração",
            nome_fantasia="Demo",
            cnpj="12345678000199",
            telefone="84990000000",
        )

    def test_loads_company_data_and_is_safe_to_repeat(self):
        call_command("load_demo_data", email=self.empresa.email)

        self.assertEqual(Produto.objects.filter(empresa=self.empresa).count(), 6)
        self.assertEqual(Cliente.objects.filter(empresa=self.empresa).count(), 5)
        self.assertEqual(Pedidos_Venda.objects.filter(empresa=self.empresa).count(), 12)

        client = self.client
        self.assertTrue(client.login(email=self.empresa.email, password="senha-de-teste"))
        response = client.get(reverse("dashboard:index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total_produtos"], 6)
        self.assertEqual(response.context["total_clientes"], 5)
        self.assertGreater(response.context["total_vendas"], 0)

        response = client.get(reverse("dashboard:vendas"))
        self.assertContains(response, "R$ 129,90")

        estoque_antes = list(
            Produto.objects.filter(empresa=self.empresa)
            .order_by("id")
            .values_list("estoque_produto__quantidade", flat=True)
        )
        with patch(
            "control.management.commands.load_demo_data.timezone.localdate",
            return_value=timezone.localdate() + timedelta(days=1),
        ):
            call_command("load_demo_data", email=self.empresa.email)

        self.assertEqual(Produto.objects.filter(empresa=self.empresa).count(), 6)
        self.assertEqual(Pedidos_Venda.objects.filter(empresa=self.empresa).count(), 12)
        estoque_depois = list(
            Produto.objects.filter(empresa=self.empresa)
            .order_by("id")
            .values_list("estoque_produto__quantidade", flat=True)
        )
        self.assertEqual(estoque_depois, estoque_antes)
