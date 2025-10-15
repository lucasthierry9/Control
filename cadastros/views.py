from django.shortcuts import render,get_object_or_404,redirect
from control.models import Cliente
from control.forms import ClienteForm
# Create your views here.


def clientes(request):
    clientes = Cliente.objects.all()
    return render(request, "cadastros/clientes.html", {"clientes": clientes})

def cadastrar_cliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("cadastros:clientes")
    else:
        form = ClienteForm()
    return render(request, "cadastros/cadastrar_cliente.html", {"form": form})
            
def editar_cliente(request, id_cliente):
    cliente = get_object_or_404(Cliente, id=id_cliente)
    form = ClienteForm(request.POST, instance=cliente)
    if form.is_valid():
        form.save()
        return redirect("cadastros:clientes")
    else:
        form = ClienteForm(instance=cliente)
    return render(request, "cadastros/editar_cliente.html", {"form": form})


def excluir_cliente(request, id_cliente=0):
    if request.method == "POST":
        cliente = get_object_or_404(Cliente, id=request.POST.get("id_cliente"))
        cliente.delete()
        return redirect('cadastros:clientes')
    else:
        cliente = get_object_or_404(Cliente, id=id_cliente)
        return render(request, "cadastros/confirma.html", {"cliente": cliente})