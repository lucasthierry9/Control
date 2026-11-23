from django.test import TestCase

from control.forms import FornecedorForm
from control.models import Fornecedor


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
