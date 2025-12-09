from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()

class Estado(models.Model):
    estado = models.CharField(max_length=2)

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
    nome = models.CharField(max_length=50)
    cpf_cnpj = models.CharField(max_length=14)
    email = models.EmailField(max_length=254, default="")
    telefone = models.CharField(max_length=11, default="")
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    cidade = models.CharField(max_length=50, default="")
    bairro = models.CharField(max_length=50, default="")
    logradouro = models.CharField(max_length=100, default="")
    numero = models.CharField(max_length=100, default="")
    complemento = models.CharField(max_length=100, blank=True)
    cep = models.CharField(max_length=8, default="")

    class Meta:
        verbose_name_plural = "Fornecedores"

    def __str__(self):
        return self.nome

class Cliente(models.Model):
    nome = models.CharField(max_length=50)
    cpf = models.CharField(max_length=11)
    email = models.EmailField(max_length=254, default="")
    telefone = models.CharField(max_length=11, default="")
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    cidade = models.CharField(max_length=50)
    bairro = models.CharField(max_length=50)
    logradouro = models.CharField(max_length=100)
    numero = models.CharField(max_length=100)
    complemento = models.CharField(max_length=100, blank=True)
    cep = models.CharField(max_length=8)

    def __str__(self):
        return self.nome

class Categoria_Produto(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.CharField(max_length=200, blank=True)

    @property
    def quantidade(self):
        return Produto.objects.filter(categoria=self).count()

    def __str__(self):
        return f"{self.nome}"

class Produto(models.Model):
    categoria = models.ForeignKey(Categoria_Produto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    imagem = models.ImageField(upload_to="imagens/", blank=True)

    def __str__(self):
        return self.nome

class Pedidos_Compra(models.Model):
    STATUS = (
        ('aberto', 'Em aberto'),
        ('processando', 'Processando'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
    )

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS, default='aberto')

class Deposito(models.Model):
    descricao = models.CharField(max_length=50)

    def __str__(self):
        return self.descricao

class Movimentacao(models.Model):
    TIPO_MOVIMENTACAO = (
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    )

    tipo = models.CharField(max_length=20, choices=TIPO_MOVIMENTACAO)
    deposito = models.ForeignKey(Deposito, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    dataehora = models.DateTimeField(default=timezone.now)
    preco_custo = models.DecimalField(max_digits=8, decimal_places=2)
    preco_compra = models.DecimalField(max_digits=8, decimal_places=2, null=True)

class Estoque_Produto(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    deposito = models.ForeignKey(Deposito, on_delete=models.CASCADE)
    quantidade = models.IntegerField()

class Vendedor(models.Model):
    nome = models.CharField(max_length=50)
    cpf = models.CharField(max_length=11)
    email = models.EmailField(max_length=254, default="")
    telefone = models.CharField(max_length=11, default="")

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

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    pagamento = models.CharField(max_length=20, choices=TIPO_PAGAMENTO)
    data = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS, default='aberto')
    peso = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    valor_frete = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    frete = models.CharField(max_length=30, choices=TIPO_FRETE, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    cidade = models.CharField(max_length=50)
    bairro = models.CharField(max_length=50)
    logradouro = models.CharField(max_length=100)
    numero = models.CharField(max_length=7)
    complemento = models.CharField(max_length=100, blank=True)
    cep = models.CharField(max_length=8)


    def total(self):
        return self.produto.preco * self.quantidade

class Funcionario(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="perfil_funcionario")
    empresa = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="funcionarios")
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11)
    telefone = models.CharField(max_length=20, blank=True)
    cargo = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nome} ({self.cargo})"