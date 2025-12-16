from django.shortcuts import render,get_object_or_404,redirect
from control.models import Cliente, Produto, Funcionario, Vendedor, Fornecedor, Categoria_Produto
from control.forms import ClienteForm, ProdutoForm, FuncionarioForm, VendedorForm, FornecedorForm, CategoriaForm
from usuarios.models import Usuario
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from control.utils import registrar_acao, ultimas_acoes_modulo

#CLIENTES
@login_required
def clientes(request):
    search = request.GET.get("search")

    clientes = Cliente.objects.all()

    if search:
        filtros = (
            Q(nome__icontains=search) |
            Q(logradouro__icontains=search) |
            Q(id__icontains=search) 
        )
        if search.isdigit() and len(search) >= 7:
            filtros |= Q(cpf__icontains=search)

        clientes = clientes.filter(filtros)

    paginator = Paginator(clientes, 10)
    numero_da_pagina = request.GET.get('p')
    clientes_paginados = paginator.get_page(numero_da_pagina)
    return render(request, "cadastros/clientes/clientes.html", {"clientes": clientes_paginados, "search": search, "historico": ultimas_acoes_modulo(request.user, 'clientes')})

@login_required
def cadastrar_cliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()

            registrar_acao(
                request.user,
                'clientes',
                f"{cliente.nome} cadastrado"
            )
            return redirect("cadastros:clientes")
    else:
        form = ClienteForm()
    return render(request, "cadastros/clientes/cadastrar_cliente.html", {"form": form, 'historico': ultimas_acoes_modulo(request.user, 'clientes',)})

def editar_cliente(request, id_cliente):
    cliente = get_object_or_404(Cliente, id=id_cliente)

    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            cliente = form.save()

            registrar_acao(
                request.user,
                'clientes',
                f"{cliente.nome} editado"
            )
            return redirect("cadastros:clientes")
    else:
        form = ClienteForm(instance=cliente)

    return render(request, "cadastros/clientes/editar_cliente.html", {"form": form, 'historico': ultimas_acoes_modulo(request.user, 'clientes')})

@login_required
def excluir_cliente(request, id_cliente=0):
    if request.method == "POST":
        ids = request.POST.getlist("ids_selecionados")
        Cliente.objects.filter(id__in=ids).delete() 
        return redirect('cadastros:clientes')
    else:
        cliente = get_object_or_404(Cliente, id=id_cliente)
        return render(request, "cadastros/clientes/confirma.html", {"cliente": cliente})
    
# ----------------------------------------------------------------------------------------

# PRODUTOS
@login_required
def produtos(request):
    search = request.GET.get("search")

    produtos = Produto.objects.all()

    if search:
        produtos = produtos.filter(
            Q(nome__icontains=search) |
            Q(categoria__nome__icontains=search) |
            Q(id__icontains=search) 
        )
    
    produtos = produtos.order_by('-id')

    paginator = Paginator(produtos, 10)
    numero_da_pagina = request.GET.get('p')
    produtos_paginados = paginator.get_page(numero_da_pagina)
    return render(request, "cadastros/produtos/produtos.html", {"produtos": produtos_paginados, "search": search, "historico": ultimas_acoes_modulo(request.user, 'produtos')})

@login_required
def cadastrar_produto(request):
    if request.method == "POST":
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            produto = form.save()

            registrar_acao(
                request.user,
                'produtos',
                f"{produto.nome} cadastrado"
            )
            return redirect("cadastros:produtos")
    else:
        form = ProdutoForm()
    return render(request, "cadastros/produtos/cadastrar_produto.html", {"form": form, "historico": ultimas_acoes_modulo(request.user, 'produtos',)})

@login_required 
def editar_produto(request, id_produto):
    produto = get_object_or_404(Produto, id=id_produto)

    if request.method == "POST":
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            produto = form.save()

            registrar_acao(
                request.user,
                'produtos',
                f"{produto.nome} editado"
            )
            return redirect("cadastros:produtos")
    else:
        form = ProdutoForm(instance=produto)

    return render(request, "cadastros/produtos/editar_produto.html", {"form": form, "historico": ultimas_acoes_modulo(request.user, 'produtos',), "produto": produto})

@login_required
def excluir_produto(request, id_produto=0):
    if request.method == "POST":
        ids = request.POST.getlist("ids_selecionados")
        Produto.objects.filter(id__in=ids).delete() 
        return redirect('cadastros:produtos')
    else:
        produto = get_object_or_404(Produto, id=id_produto)
        return render(request, "cadastros/produtos/confirma.html", {"produto": produto})

# ----------------------------------------------------------------------------------------

# FUNCIONÁRIOS
@login_required
def funcionarios(request):
    search = request.GET.get("search")

    funcionarios = Funcionario.objects.all()

    if search:
        filtros = (
            Q(nome__icontains=search) |
            Q(cargo__icontains=search) |
            Q(id__icontains=search) 
        )
        if search.isdigit() and len(search) >= 7:
            filtros |= Q(cpf__icontains=search)

        funcionarios = funcionarios.filter(filtros)

    paginator = Paginator(funcionarios, 10)
    numero_da_pagina = request.GET.get('p')
    funcionarios = paginator.get_page(numero_da_pagina)
    return render(request, "cadastros/funcionarios/funcionarios.html", {"funcionarios": funcionarios, "search": search, "historico": ultimas_acoes_modulo(request.user, 'funcionarios')})

@login_required
def cadastrar_funcionario(request):
    if request.method == "POST":
        form = FuncionarioForm(request.POST)
        if form.is_valid():

            func_user = Usuario.objects.create_user(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['senha'],
                tipo='funcionario',
                razao_social="Funcionário",
                nome_fantasia=form.cleaned_data['nome'],
                telefone=form.cleaned_data['telefone'],
                cnpj=None
            )

            Funcionario.objects.create(
                user=func_user,
                empresa=request.user,
                nome=form.cleaned_data['nome'],
                cpf=form.cleaned_data['cpf'],
                telefone=form.cleaned_data['telefone'],
                cargo=form.cleaned_data['cargo']
            )

            return redirect("cadastros:funcionarios")

    else:
        form = FuncionarioForm()

    return render(request, "cadastros/funcionarios/cadastrar_funcionario.html", {"form": form})

@login_required
def editar_funcionario(request, id_funcionario):
    funcionario = get_object_or_404(Funcionario, id=id_funcionario)
    if request.method == "POST":
        form = FuncionarioForm(request.POST, instance=funcionario)
        if form.is_valid():
            funcionario = form.save()

            registrar_acao(
                request.user,
                'funcionarios',
                f"{funcionario.nome} editado"
            )
            return redirect("cadastros:funcionarios")
    else:
        form = FuncionarioForm(instance=funcionario)
    return render(request, "cadastros/funcionarios/editar_funcionario.html", {"form": form, "historico": ultimas_acoes_modulo(request.user, 'funcionarios'), "funcionario": funcionario})

@login_required
def excluir_funcionario(request, id_funcionario=0):
    if request.method == "POST":
        ids = request.POST.getlist("ids_selecionados")
        Funcionario.objects.filter(id__in=ids).delete() 
        return redirect('cadastros:funcionarios')
    else:
        funcionario = get_object_or_404(Funcionario, id=id_funcionario)
        return render(request, "cadastros/funcionarios/confirma.html", {"funcionario": funcionario})

# ----------------------------------------------------------------------------------------

# VENDEDORES
@login_required
def vendedores(request):
    search = request.GET.get("search")

    vendedores = Vendedor.objects.all()

    if search:
        filtros = (
            Q(nome__icontains=search) |
            Q(id__icontains=search) 
        )
        if search.isdigit():
            if len(search) >= 7:
                filtros |= Q(cpf__icontains=search)

            if len(search) >= 7:
                filtros |= Q(telefone__icontains=search)
            

        vendedores = vendedores.filter(filtros)

    paginator = Paginator(vendedores, 10)
    numero_da_pagina = request.GET.get('p')
    vendedores = paginator.get_page(numero_da_pagina)
    return render(request, "cadastros/vendedores/vendedores.html", {"vendedores": vendedores, "search": search, "historico": ultimas_acoes_modulo(request.user, 'vendedores')})

@login_required
def cadastrar_vendedor(request):
    if request.method == "POST":
        form = VendedorForm(request.POST)
        if form.is_valid():
            vendedor = form.save()

            registrar_acao(
                request.user,
                'vendedores',
                f"{vendedor.nome} cadastrado"
            )
            return redirect("cadastros:vendedores")
    else:
        form = VendedorForm()
    return render(request, "cadastros/vendedores/cadastrar_vendedor.html", {"form": form, "historico": ultimas_acoes_modulo(request.user, 'vendedores')})

@login_required 
def editar_vendedor(request, id_vendedor):
    vendedor = get_object_or_404(Vendedor, id=id_vendedor)

    if request.method == "POST":
        form = VendedorForm(request.POST, instance=vendedor)
        if form.is_valid():
            vendedor = form.save()

            registrar_acao(
                request.user,
                'vendedores',
                f"{vendedor.nome} editado"
            )
            return redirect("cadastros:vendedores")
    else:
        form = VendedorForm(instance=vendedor)

    return render(request, "cadastros/vendedores/editar_vendedor.html", {"form": form, "historico": ultimas_acoes_modulo(request.user, 'vendedores'), "vendedor": vendedor})

@login_required
def excluir_vendedor(request, id_vendedor=0):
    if request.method == "POST":
        ids = request.POST.getlist("ids_selecionados")
        Vendedor.objects.filter(id__in=ids).delete() 
        return redirect('cadastros:vendedores')
    else:
        vendedor = get_object_or_404(Vendedor, id=id_vendedor)
        return render(request, "cadastros/vendedores/confirma.html", {"vendedor": vendedor})
    
# FORNECEDOR -----------------------
@login_required
def fornecedores(request):
    search = request.GET.get("search")

    fornecedores = Fornecedor.objects.all()

    if search:
        filtros = (
            Q(nome__icontains=search) |
            Q(logradouro__icontains=search) |
            Q(id__icontains=search) 
        )
        if search.isdigit() and len(search) >= 7:
            filtros |= Q(cpf_cnpj__icontains=search)

        fornecedores = fornecedores.filter(filtros)

    paginator = Paginator(fornecedores, 10)
    numero_da_pagina = request.GET.get('p')
    fornecedores = paginator.get_page(numero_da_pagina)
    return render(request, "cadastros/fornecedores/fornecedores.html", {"fornecedores": fornecedores, "search": search, "historico": ultimas_acoes_modulo(request.user,'fornecedores')})

@login_required
def cadastrar_fornecedor(request):
    if request.method == "POST":
        form = FornecedorForm(request.POST)
        if form.is_valid():
            fornecedor = form.save()

            registrar_acao(
                request.user,
                'fornecedores',
                f"{fornecedor.nome} cadastrado"
            )
            return redirect("cadastros:fornecedores")
    else:
        form = FornecedorForm()
    return render(request, "cadastros/fornecedores/cadastrar_fornecedor.html", {"form": form, "historico": ultimas_acoes_modulo(request.user, 'fornecedores')})

@login_required  
def editar_fornecedor(request, id_fornecedor):
    fornecedor = get_object_or_404(Fornecedor, id=id_fornecedor)
    if request.method == "POST":
        form = FornecedorForm(request.POST, instance=fornecedor)
        if form.is_valid():
            fornecedor = form.save()

            registrar_acao(
                request.user,
                'fornecedores',
                f"{fornecedor.nome} editado"
            )
            return redirect("cadastros:fornecedores")
    else:
        form = FornecedorForm(instance=fornecedor)
    return render(request, "cadastros/fornecedores/editar_fornecedor.html", {"form": form, "historico": ultimas_acoes_modulo(request.user, 'fornecedores'), "fornecedor": fornecedor})

@login_required
def excluir_fornecedor(request, id_fornecedor=0):
    if request.method == "POST":
        ids = request.POST.getlist("ids_selecionados")
        Fornecedor.objects.filter(id__in=ids).delete() 
        return redirect('cadastros:fornecedores')
    else:
        fornecedor = get_object_or_404(Fornecedor, id=id_fornecedor)
        return render(request, "cadastros/fornecedores/confirma.html", {"fornecedor": fornecedor})
    
# ----------------------------------------------------------------------------------------

# CATEGORIA ------------------------------------------------------------------------------
@login_required
def categorias(request):
    search = request.GET.get("search")

    categorias = Categoria_Produto.objects.all()

    if search:
        categorias = categorias.filter(
            Q(nome__icontains=search) |
            Q(descricao__icontains=search) |
            Q(id__icontains=search) 
        )
    
    categorias = categorias.order_by('-id')

    paginator = Paginator(categorias, 10)
    numero_da_pagina = request.GET.get('p')
    categorias = paginator.get_page(numero_da_pagina)
    return render(request, "cadastros/categorias/categorias.html", {"categorias": categorias, "search": search, "historico": ultimas_acoes_modulo(request.user, 'categorias')})

@login_required
def cadastrar_categoria(request):
    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save()

            registrar_acao(
                request.user,
                'categorias',
                f"{categoria.nome} cadastrado"
            )
            return redirect("cadastros:categorias")
    else:
        form = CategoriaForm()
    return render(request, "cadastros/categorias/cadastrar_categoria.html", {"form": form, "historico": ultimas_acoes_modulo(request.user, 'categorias')})

@login_required
def editar_categoria(request, id_categoria):
    categoria = get_object_or_404(Categoria_Produto, id=id_categoria)

    if request.method == "POST":
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            categoria = form.save()

            registrar_acao(
                request.user,
                'categorias',
                f"{categoria.nome} editado"
            )
            return redirect("cadastros:categorias")
    else:
        form = CategoriaForm(instance=categoria)

    return render(request, "cadastros/categorias/editar_categoria.html", {"form": form, "historico": ultimas_acoes_modulo(request.user, 'categorias'), "categoria": categoria})

@login_required
def excluir_categoria(request, id_categoria=0):
    if request.method == "POST":
        ids = request.POST.getlist("ids_selecionados")
        Categoria_Produto.objects.filter(id__in=ids).delete() 
        return redirect('cadastros:categorias')
    else:
        categoria = get_object_or_404(Categoria_Produto, id=id_categoria)
        return render(request, "cadastros/categorias/confirma.html", {"categoria": categoria})
    
# ----------------------------------------------------------------------------------------