from django.shortcuts import render,get_object_or_404,redirect
from control.models import Cliente, Produto
from control.forms import ClienteForm, ProdutoForm

#CLIENTES

def clientes(request):
    clientes = Cliente.objects.all()
    return render(request, "cadastros/clientes/clientes.html", {"clientes": clientes})

def cadastrar_cliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("cadastros:clientes")
    else:
        form = ClienteForm()
    return render(request, "cadastros/clientes/cadastrar_cliente.html", {"form": form})
            
def editar_cliente(request, id_cliente):
    cliente = get_object_or_404(Cliente, id=id_cliente)
    form = ClienteForm(request.POST, instance=cliente)
    if form.is_valid():
        form.save()
        return redirect("cadastros:clientes")
    else:
        form = ClienteForm(instance=cliente)
    return render(request, "cadastros/clientes/editar_cliente.html", {"form": form})


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

def produtos(request):
    produtos = Produto.objects.all()
    return render(request, "cadastros/produtos/produtos.html", {"produtos": produtos})

def cadastrar_produto(request):
    if request.method == "POST":
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("cadastros:produtos")
    else:
        form = ProdutoForm()
    return render(request, "cadastros/produtos/cadastrar_produto.html", {"form": form})
            
def editar_produto(request, id_produto):
    produto = get_object_or_404(Produto, id=id_produto)
    form = ProdutoForm(request.POST, instance=produto)
    if form.is_valid():
        form.save()
        return redirect("cadastros:produtos")
    else:
        form = ProdutoForm(instance=produto)
    return render(request, "cadastros/produtos/editar_produto.html", {"form": form})


def excluir_produto(request, id_produto=0):
    if request.method == "POST":
        produto = get_object_or_404(Produto, id=request.POST.get("id_produto"))
        produto.delete()
        return redirect('cadastros:produtos')
    else:
        produto = get_object_or_404(Produto, id=id_produto)
        return render(request, "cadastros/produtos/confirma.html", {"produto": produto})

# ----------------------------------------------------------------------------------------