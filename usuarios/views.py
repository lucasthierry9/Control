from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from usuarios.forms import UserForm
from .models import Usuario

def cadastrar_usuario(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("usuarios:login")
    else:
        form = UserForm()
    return render(request, "registration/register.html", {"form": form})

@login_required
def perfil(request):
    return render(request, "registration/perfil.html")

@login_required
def editar_perfil(request, id_usuario):
    usuario = get_object_or_404(Usuario, id=id_usuario)

    if request.method == "POST":
        usuario.nome_fantasia = request.POST.get("nome_fantasia")
        usuario.email = request.POST.get("email")
        usuario.telefone = request.POST.get("telefone")
        usuario.endereco = request.POST.get("endereco")
        usuario.nome_admin = request.POST.get("nome_admin")
        usuario.email_admin = request.POST.get("email_admin")
        usuario.telefone_admin = request.POST.get("telefone_admin")
        usuario.cpf_admin = request.POST.get("cpf_admin")

        if "imagem_perfil" in request.FILES:
            usuario.imagem_perfil = request.FILES["imagem_perfil"]

        usuario.save()
        return redirect("usuarios:perfil")

    return render(request, "registration/editar_perfil.html", {"usuario": usuario})


