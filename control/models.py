from django.db import models
from django.utils import timezone

class Estado(models.Model):
    estado = models.CharField(max_length=50)

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

    class Meta:
        verbose_name_plural = "Fornecedores"

    def __str__(self):
        return self.nome

class Tel_Fornecedor(models.Model):
    telefone = models.CharField(max_length=11)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)

class Email_Fornecedor(models.Model):
    email = models.EmailField(max_length=254)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)

class Cliente(models.Model):
    nome = models.CharField(max_length=50)
    cpf = models.CharField(max_length=11)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE)
    bairro = models.ForeignKey(Bairro, on_delete=models.CASCADE)
    logradouro = models.CharField(max_length=100)
    número = models.CharField(max_length=100)
    complemento = models.CharField(max_length=100, blank=True)
    cep = models.CharField(max_length=8)

    def __str__(self):
        return self.nome

class Tel_Cliente(models.Model):
    telefone = models.CharField(max_length=11)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

class Email_Cliente(models.Model):
    email = models.EmailField(max_length=254)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

class Categoria_Produto(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.TextField(max_length=100, blank=True)

    @property
    def quantidade(self):
        return Produto.objects.filter(categoria=self).count()

    def __str__(self):
        return f"{self.nome}"

class Produto(models.Model):
    categoria = models.ForeignKey(Categoria_Produto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    imagem = models.ImageField(upload_to="imagens/")
    quantidade = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nome

class Pedidos_Compra(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    valor = models.DecimalField(max_digits=8, decimal_places=2)

class Deposito(models.Model):
    descricao = models.CharField(max_length=50)

class Tipos_Movimentacao(models.Model):
    tipo = models.CharField(max_length=50)

class Movimentacao(models.Model):
    tipo = models.ForeignKey(Tipos_Movimentacao, on_delete=models.CASCADE)
    deposito = models.ForeignKey(Deposito, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    dataehora = models.DateTimeField()
    preco_custo = models.DecimalField(max_digits=8, decimal_places=2)

class Estoque_Produto(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    deposito = models.ForeignKey(Deposito, on_delete=models.CASCADE)
    quantidade = models.IntegerField()

class Vendedor(models.Model):
    nome = models.CharField(max_length=50)
    cpf = models.CharField(max_length=11)
    class Meta:
        verbose_name_plural = "Vendedores"
    def __str__(self):
        return self.nome

class Tel_Vendedor(models.Model):
    telefone = models.CharField(max_length=11)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)

class Email_Vendedor(models.Model):
    email = models.EmailField(max_length=254)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)

class Pedidos_Venda(models.Model):
    STATUS_CHOICES = (
        ('aberto', 'Em aberto'),
        ('processando', 'Processando'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
    )

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    bairro = models.ForeignKey(Bairro, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    logradouro = models.CharField(max_length=100)
    numero = models.CharField(max_length=7)
    pagamento = models.CharField(max_length=20)
    data = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aberto')

    def total(self):
        return self.produto.preco * self.quantidade

class Funcionario(models.Model):
    nome = models.CharField(max_length=50)
    cpf = models.CharField(max_length=11)
    cargo = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class Tel_Funcionario(models.Model):
    telefone = models.CharField(max_length=11)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)

class Email_Funcionario(models.Model):
    email = models.EmailField(max_length=254)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)