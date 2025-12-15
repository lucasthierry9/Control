from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from usuarios.forms import UserForm
from .models import Usuario
from control.models import Funcionario
from django.contrib.auth.views import LoginView
from django.contrib.auth import login


def cadastrar_usuario(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("usuarios:login")
    else:
        form = UserForm()
    return render(request, "registration/cadastro.html", {"form": form})


@login_required
def perfil(request):
    user = request.user
    
    # Caso seja empresa → envia apenas os dados do usuário
    if user.tipo == 'empresa':
        template = 'registration/perfil_empresa.html'
        context = {
            'user': user
        }
    
    # Caso seja funcionário → envia dados de usuário + funcionário
    else:
        template = 'registration/perfil_funcionario.html'

        try:
            funcionario = Funcionario.objects.get(user=user)
        except Funcionario.DoesNotExist:
            funcionario = None
        context = {
            'user': user,
            'funcionario': funcionario
        }

    return render(request, template, context)

@login_required
def editar_perfil(request, id_usuario):
    user = request.user
    funcionario = None
    
    if user.tipo =='empresa':
        usuario = get_object_or_404(Usuario, id=id_usuario)
        template = 'registration/editar_perfil.html'
        
        if request.method == "POST":
            usuario.nome_fantasia = request.POST.get("nome_fantasia")
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
    else:
        usuario = get_object_or_404(Usuario, id=id_usuario)
        funcionario = Funcionario.objects.filter(user=user).first()
        template = 'registration/editar_perfil_funcionario.html'

        if request.method == "POST":
            usuario.telefone = request.POST.get("telefone")
            funcionario.nome = request.POST.get("nome")
            funcionario.cargo = request.POST.get("cargo")

            if "imagem_perfil" in request.FILES:
                usuario.imagem_perfil = request.FILES["imagem_perfil"]

            usuario.save()
            funcionario.save()
            return redirect("usuarios:perfil")
    

    return render(request, template, {"usuario": usuario, "funcionario": funcionario})



