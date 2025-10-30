from django.shortcuts import render,get_object_or_404,redirect
from control.models import Cliente, Produto, Funcionario, Vendedor, Fornecedor
from control.forms import ClienteForm, ProdutoForm, FuncionarioForm, VendedorForm, FornecedorForm
from django.contrib.auth.decorators import login_required

#CLIENTES
@login_required
def clientes(request):
    clientes = Cliente.objects.all()
    return render(request, "cadastros/clientes/clientes.html", {"clientes": clientes})

@login_required
def cadastrar_cliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("cadastros:clientes")
    else:
        form = ClienteForm()
    return render(request, "cadastros/clientes/cadastrar_cliente.html", {"form": form})

@login_required      
def editar_cliente(request, id_cliente):
    cliente = get_object_or_404(Cliente, id=id_cliente)
    form = ClienteForm(request.POST, instance=cliente)
    if form.is_valid():
        form.save()
        return redirect("cadastros:clientes")
    else:
        form = ClienteForm(instance=cliente)
    return render(request, "cadastros/clientes/editar_cliente.html", {"form": form})

@login_required
def excluir_cliente(request, id_cliente=0):
    if request.method == "POST":
        cliente = get_object_or_404(Cliente, id=request.POST.get("id_cliente"))
        cliente.delete()
        return redirect('cadastros:clientes')
    else:
        cliente = get_object_or_404(Cliente, id=id_cliente)
        return render(request, "cadastros/clientes/confirma.html", {"cliente": cliente})

# ----------------------------------------------------------------------------------------

# PRODUTOS
@login_required
def produtos(request):
    produtos = Produto.objects.all()
    return render(request, "cadastros/produtos/produtos.html", {"produtos": produtos})

@login_required
def cadastrar_produto(request):
    if request.method == "POST":
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("cadastros:produtos")
    else:
        form = ProdutoForm()
    return render(request, "cadastros/produtos/cadastrar_produto.html", {"form": form})

@login_required 
def editar_produto(request, id_produto):
    produto = get_object_or_404(Produto, id=id_produto)
    form = ProdutoForm(request.POST, instance=produto)
    if form.is_valid():
        form.save()
        return redirect("cadastros:produtos")
    else:
        form = ProdutoForm(instance=produto)
    return render(request, "cadastros/produtos/editar_produto.html", {"form": form})

@login_required
def excluir_produto(request, id_produto=0):
    if request.method == "POST":
        produto = get_object_or_404(Produto, id=request.POST.get("id_produto"))
        produto.delete()
        return redirect('cadastros:produtos')
    else:
        produto = get_object_or_404(Produto, id=id_produto)
        return render(request, "cadastros/produtos/confirma.html", {"produto": produto})

# ----------------------------------------------------------------------------------------

# FUNCIONÁRIOS
@login_required
def funcionarios(request):
    funcionarios = Funcionario.objects.all()
    return render(request, "cadastros/funcionarios/funcionarios.html", {"funcionarios": funcionarios})

@login_required
def cadastrar_funcionario(request):
    if request.method == "POST":
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("cadastros:funcionarios")
    else:
        form = FuncionarioForm()
    return render(request, "cadastros/funcionarios/cadastrar_funcionario.html", {"form": form})

@login_required
def editar_funcionario(request, id_funcionario):
    funcionario = get_object_or_404(Funcionario, id=id_funcionario)
    form = FuncionarioForm(request.POST, instance=funcionario)
    if form.is_valid():
        form.save()
        return redirect("cadastros:funcionarios")
    else:
        form = FuncionarioForm(instance=funcionario)
    return render(request, "cadastros/funcionarios/editar_funcionario.html", {"form": form})

@login_required
def excluir_funcionario(request, id_funcionario=0):
    if request.method == "POST":
        funcionario = get_object_or_404(Funcionario, id=request.POST.get("id_funcionario"))
        funcionario.delete()
        return redirect('cadastros:funcionarios')
    else:
        funcionario = get_object_or_404(Funcionario, id=id_funcionario)
        return render(request, "cadastros/funcionarios/confirma.html", {"funcionario": funcionario})

# ----------------------------------------------------------------------------------------

# VENDEDORES
@login_required
def vendedores(request):
    vendedores = Vendedor.objects.all()
    return render(request, "cadastros/vendedores/vendedores.html", {"vendedores": vendedores})

@login_required
def cadastrar_vendedor(request):
    if request.method == "POST":
        form = VendedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("cadastros:vendedores")
    else:
        form = VendedorForm()
    return render(request, "cadastros/vendedores/cadastrar_vendedor.html", {"form": form})

@login_required         
def editar_vendedor(request, id_vendedor):
    vendedor = get_object_or_404(Vendedor, id=id_vendedor)
    form = VendedorForm(request.POST, instance=vendedor)
    if form.is_valid():
        form.save()
        return redirect("cadastros:vendedores")
    else:
        form = VendedorForm(instance=vendedor)
    return render(request, "cadastros/vendedores/editar_vendedor.html", {"form": form})

@login_required
def excluir_vendedor(request, id_vendedor=0):
    if request.method == "POST":
        vendedor = get_object_or_404(Vendedor, id=request.POST.get("id_vendedor"))
        vendedor.delete()
        return redirect('cadastros:vendedores')
    else:
        vendedor = get_object_or_404(Vendedor, id=id_vendedor)
        return render(request, "cadastros/vendedores/confirma.html", {"vendedor": vendedor})
    
# FORNECEDOR -----------------------
@login_required
def fornecedores(request):
    fornecedores = Fornecedor.objects.all()
    return render(request, "cadastros/fornecedores/fornecedores.html", {"fornecedores": fornecedores})

@login_required
def cadastrar_fornecedor(request):
    if request.method == "POST":
        form = FornecedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("cadastros:fornecedores")
    else:
        form = FornecedorForm()
    return render(request, "cadastros/fornecedores/cadastrar_fornecedor.html", {"form": form})

@login_required  
def editar_fornecedor(request, id_fornecedor):
    fornecedor = get_object_or_404(Fornecedor, id=id_fornecedor)
    form = FornecedorForm(request.POST, instance=fornecedor)
    if form.is_valid():
        form.save()
        return redirect("cadastros:fornecedores")
    else:
        form = FornecedorForm(instance=fornecedor)
    return render(request, "cadastros/fornecedores/editar_fornecedor.html", {"form": form})

@login_required
def excluir_fornecedor(request, id_fornecedor=0):
    if request.method == "POST":
        fornecedor = get_object_or_404(Fornecedor, id=request.POST.get("id_fornecedor"))
        fornecedor.delete()
        return redirect('cadastros:fornecedores')
    else:
        fornecedor = get_object_or_404(Fornecedor, id=id_fornecedor)
        return render(request, "cadastros/fornecedores/confirma.html", {"fornecedor": fornecedor})
    
# ----------------------------------------------------------------------------------------