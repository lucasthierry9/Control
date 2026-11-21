from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from usuarios.models import Usuario
from django.core.exceptions import ValidationError
from django.db import transaction
User = get_user_model()

class Estado(models.Model):
    ESTADOS_CHOICES = [
    ('AC', 'AC'),
    ('AL', 'AL'),
    ('AM', 'AM'),
    ('AP', 'AP'),
    ('BA', 'BA'),
    ('CE', 'CE'),
    ('DF', 'DF'),
    ('ES', 'ES'),
    ('GO', 'GO'),
    ('MA', 'MA'),
    ('MG', 'MG'),
    ('MS', 'MS'),
    ('MT', 'MT'),
    ('PA', 'PA'),
    ('PB', 'PB'),
    ('PE','PE'),
    ('PI', 'PI'),
    ('PR', 'PR'),
    ('RJ', 'RJ'),
    ('RN', 'RN'),
    ('RO', 'RO'),
    ('RR', 'RR'),
    ('RS', 'RS'),
    ('SC', 'SC'),
    ('SE', 'SE'),
    ('SP', 'SP'),
    ('TO', 'TO'),
    ]
    estado = models.CharField(max_length=2, choices=ESTADOS_CHOICES)

    def __str__(self):
        return self.estado

class Cidade(models.Model):
    cidade = models.CharField(max_length=50)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)

    def __str__(self):
        return self.cidade

class Bairro(models.Model):
    bairro = models.CharField(max_length=50)
    cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE)

    def __str__(self):
        return self.bairro

class Fornecedor(models.Model):
    empresa = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="fornecedores")
    nome = models.CharField(max_length=50)
    cpf_cnpj = models.CharField(max_length=14)
    email = models.EmailField(max_length=254, default="")
    telefone = models.CharField(max_length=11, default="")
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, null=True, blank=True)
    cidade = models.CharField(max_length=50, default="")
    bairro = models.CharField(max_length=50, default="")
    logradouro = models.CharField(max_length=100, default="")
    numero = models.CharField(max_length=100, default="")
    complemento = models.CharField(max_length=100, blank=True)
    cep = models.CharField(max_length=8, default="")
    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Fornecedores"

    def __str__(self):
        return self.nome

class Cliente(models.Model):
    empresa = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="clientes")
    nome = models.CharField(max_length=50)
    cpf = models.CharField(max_length=11)
    email = models.EmailField(max_length=254, default="")
    telefone = models.CharField(max_length=11, default="")
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, null=True, blank=True)
    cidade = models.CharField(max_length=50, blank=True)
    bairro = models.CharField(max_length=50, blank=True)
    logradouro = models.CharField(max_length=100, blank=True)
    numero = models.CharField(max_length=100, blank=True)
    complemento = models.CharField(max_length=100, blank=True)
    cep = models.CharField(max_length=8, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Categoria_Produto(models.Model):
    empresa = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="categorias_produto")
    nome = models.CharField(max_length=50)
    descricao = models.CharField(max_length=200, blank=True)
    

    @property
    def quantidade(self):
        return Produto.objects.filter(categoria=self).count()

    def __str__(self):
        return f"{self.nome}"

class Produto(models.Model):
    empresa = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="produtos")
    categoria = models.ForeignKey(Categoria_Produto, on_delete=models.PROTECT)
    nome = models.CharField(max_length=50)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    imagem = models.ImageField(upload_to="imagens/", blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Pedidos_Compra(models.Model):
    STATUS = (
        ('aberto', 'Em aberto'),
        ('processando', 'Processando'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
    )

    empresa = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="pedidos_compra")
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.PROTECT)
    deposito = models.ForeignKey('Deposito', on_delete=models.PROTECT, null=True, blank=True)
    quantidade = models.IntegerField()
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS, default='aberto')
    data = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            old = Pedidos_Compra.objects.select_for_update().filter(pk=self.pk).first() if self.pk else None
            if old and old.status == 'concluido':
                self._ajustar_estoque(old, reverter=True)
            super().save(*args, **kwargs)
            if self.status == 'concluido':
                self._ajustar_estoque(self)

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            if self.status == 'concluido':
                self._ajustar_estoque(self, reverter=True)
            return super().delete(*args, **kwargs)

    @staticmethod
    def _ajustar_estoque(pedido, reverter=False):
        deposito = pedido.deposito
        if deposito is None:
            deposito = Deposito.objects.filter(empresa=pedido.empresa).first() if pedido.empresa_id else Deposito.objects.first()
        if deposito is None:
            deposito = Deposito.objects.create(descricao="Estoque Principal", empresa=pedido.empresa)
        estoque, _ = Estoque_Produto.objects.select_for_update().get_or_create(
            produto=pedido.produto, deposito=deposito, defaults={'quantidade': 0}
        )
        estoque.quantidade += -pedido.quantidade if reverter else pedido.quantidade
        estoque.save(update_fields=['quantidade'])
    
class Deposito(models.Model):
    empresa = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="depositos")
    descricao = models.CharField(max_length=50)


    def __str__(self):
        return self.descricao

class Movimentacao(models.Model):
    TIPO_MOVIMENTACAO = (
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    )

    tipo = models.CharField(max_length=20, choices=TIPO_MOVIMENTACAO)
    empresa = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="movimentacoes")
    deposito = models.ForeignKey(Deposito, on_delete=models.PROTECT)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.IntegerField()
    dataehora = models.DateTimeField(default=timezone.now)
    preco_custo = models.DecimalField(max_digits=8, decimal_places=2)
    preco_compra = models.DecimalField(max_digits=8, decimal_places=2, null=True)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            old = Movimentacao.objects.select_for_update().filter(pk=self.pk).first() if self.pk else None
            if old:
                self._ajustar_estoque(old, reverter=True)
            super().save(*args, **kwargs)
            self._ajustar_estoque(self)

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            self._ajustar_estoque(self, reverter=True)
            return super().delete(*args, **kwargs)

    @staticmethod
    def _ajustar_estoque(mov, reverter=False):
        estoque, _ = Estoque_Produto.objects.select_for_update().get_or_create(
            produto=mov.produto, deposito=mov.deposito, defaults={'quantidade': 0}
        )
        multiplicador = -1 if reverter else 1
        delta = mov.quantidade if mov.tipo == 'entrada' else -mov.quantidade
        estoque.quantidade += delta * multiplicador
        if estoque.quantidade < 0:
            raise ValidationError("A movimentação não pode deixar o estoque negativo.")
        estoque.save(update_fields=['quantidade'])

class Estoque_Produto(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    deposito = models.ForeignKey(Deposito, on_delete=models.PROTECT)
    quantidade = models.IntegerField()

class Vendedor(models.Model):
    empresa = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="vendedores")
    nome = models.CharField(max_length=50)
    cpf = models.CharField(max_length=11)
    email = models.EmailField(max_length=254, default="")
    telefone = models.CharField(max_length=11, default="")
    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Vendedores"
    def __str__(self):
        return self.nome

class Pedidos_Venda(models.Model):
    STATUS = (
        ('aberto', 'Em aberto'),
        ('processando', 'Processando'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
    )

    TIPO_PAGAMENTO = (
    ('pix', 'Pix'),
    ('dinheiro', 'Dinheiro'),
    ('credito', 'Cartão de Crédito'),
    ('debito', 'Cartão de Débito'),
    ('boleto', 'Boleto'),
    )

    TIPO_FRETE = (
    ('cif', 'CIF - Frete Incluso'),
    ('fob', 'FOB - Frete por Conta do Cliente'),
    ('retirar', 'Retirar no Local'),
    )

    empresa = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="pedidos_venda")
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.PROTECT)
    quantidade = models.IntegerField()
    pagamento = models.CharField(max_length=20, choices=TIPO_PAGAMENTO)
    data = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS, default='aberto')
    peso = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    valor_frete = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    frete = models.CharField(max_length=30, choices=TIPO_FRETE, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, null=True, blank=True)
    cidade = models.CharField(max_length=50, blank=True)
    bairro = models.CharField(max_length=50, blank=True)
    logradouro = models.CharField(max_length=100, blank=True)
    numero = models.CharField(max_length=7, blank=True)
    complemento = models.CharField(max_length=100, blank=True)
    cep = models.CharField(max_length=8, blank=True)
    preco_unitario = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)


    def total(self):
        preco = self.preco_unitario if self.preco_unitario is not None else self.produto.preco
        frete = self.valor_frete or 0
        return preco * self.quantidade + frete

    def save(self, *args, **kwargs):
        if self.preco_unitario is None:
            self.preco_unitario = self.produto.preco
        with transaction.atomic():
            old = Pedidos_Venda.objects.select_for_update().filter(pk=self.pk).first() if self.pk else None
            if old and old.status == 'concluido':
                self._ajustar_estoque(old, reverter=True)
            super().save(*args, **kwargs)
            if self.status == 'concluido':
                self._ajustar_estoque(self)

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            if self.status == 'concluido':
                self._ajustar_estoque(self, reverter=True)
            return super().delete(*args, **kwargs)

    @staticmethod
    def _ajustar_estoque(pedido, reverter=False):
        deposito = Estoque_Produto.objects.filter(produto=pedido.produto).select_related('deposito').first()
        if deposito is None:
            deposito_obj = Deposito.objects.filter(empresa=pedido.empresa).first() if pedido.empresa_id else Deposito.objects.first()
            if deposito_obj is None:
                deposito_obj = Deposito.objects.create(descricao="Estoque Principal")
            estoque, _ = Estoque_Produto.objects.select_for_update().get_or_create(
                produto=pedido.produto, deposito=deposito_obj, defaults={'quantidade': 0}
            )
        else:
            estoque = Estoque_Produto.objects.select_for_update().get(pk=deposito.pk)
        delta = pedido.quantidade if reverter else -pedido.quantidade
        estoque.quantidade += delta
        if estoque.quantidade < 0:
            raise ValidationError("A venda não pode deixar o estoque negativo.")
        estoque.save(update_fields=['quantidade'])

class Funcionario(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="perfil_funcionario")
    empresa = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="funcionarios")
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11)
    telefone = models.CharField(max_length=20, blank=True)
    cargo = models.CharField(max_length=50)
    

    def __str__(self):
        return f"{self.nome} ({self.cargo})"
    
    
class HistoricoAcao(models.Model):
    MODULOS = (
        ('clientes', 'Clientes'),
        ('produtos', 'Produtos'),
        ('vendedores', 'Vendedores'),
        ('funcionarios', 'Funcionarios'),
        ('categorias', 'Categorias'),
        ('fornecedores', 'Fornecedores'),
    )

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    modulo = models.CharField(max_length=20, choices=MODULOS)
    descricao = models.CharField(max_length=255)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.modulo}] {self.descricao}"