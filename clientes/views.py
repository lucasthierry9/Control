from django.shortcuts import render,get_object_or_404,redirect
from control.models import Cliente
from control.forms import ClienteForm
# Create your views here.
def login(request):
    return render(request, "clientes/login.html")

def clientes(request):
    clientes = Cliente.objects.all()
    return render(request, "clientes/clientes.html", {"clientes": clientes})

def cadastrar_cliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("clientes")
    else:
        form = ClienteForm()
    return render(request, "clientes/cadastrar_cliente.html", {"form": form})
            
def editar_cliente(request, id_cliente):
    cliente = get_object_or_404(Cliente, id=id_cliente)
    form = ClienteForm(request.POST, instance=cliente)
    if form.is_valid():
        form.save()
        return redirect("clientes")
    else:
        form = ClienteForm(instance=cliente)
    return render(request, "clientes/editar_cliente.html", {"form": form})


def excluir_cliente(request, id_cliente=0):
    if request.method == "POST":
        cliente = get_object_or_404(Cliente, id=request.POST.get("id_cliente"))
        cliente.delete()
        return redirect('clientes')
    else:
        cliente = get_object_or_404(Cliente, id=id_cliente)
        return render(request, "clientes/confirma.html", {"cliente": cliente})