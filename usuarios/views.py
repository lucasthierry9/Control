from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from usuarios.forms import UserForm, ImagemPerfilForm
from .models import Usuario
from control.models import Funcionario, Pedidos_Venda, Produto
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import Group


def cadastrar_usuario(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.tipo = 'empresa'
            user.save()

            try:
                grupo_empresa = Group.objects.get(name='Empresa')
                user.groups.add(grupo_empresa)
            except Group.DoesNotExist:
                pass

            messages.success(
                request,
                "Seu cadastro foi realizado com sucesso."
            )
            return redirect("usuarios:login")

    else:
        email_inicial = request.GET.get("email")

        form = UserForm(initial={
            'email': email_inicial
        })

    return render(request, "registration/cadastro.html", {"form": form})


@login_required
def perfil(request):

    total_vendas = Pedidos_Venda.objects.filter(status='concluido').count()

    total_produtos = Produto.objects.count()

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
            'funcionario': funcionario,
            'total_vendas': total_vendas,
            'total_produtos': total_produtos,
        }

    return render(request, template, context)

@login_required
def editar_perfil(request, id_usuario):
    user = request.user
    funcionario = None

    usuario = get_object_or_404(Usuario, id=id_usuario)

    if user.tipo == 'empresa':
        template = 'registration/editar_perfil.html'
    else:
        template = 'registration/editar_perfil_funcionario.html'
        funcionario = Funcionario.objects.filter(user=user).first()

    if request.method == "POST":
        imagem_form = ImagemPerfilForm(
            request.POST,
            request.FILES,
            instance=usuario
        )

        usuario.nome_fantasia = request.POST.get("nome_fantasia")
        usuario.telefone = request.POST.get("telefone")
        usuario.endereco = request.POST.get("endereco")
        usuario.nome_admin = request.POST.get("nome_admin")
        usuario.email_admin = request.POST.get("email_admin")
        usuario.telefone_admin = request.POST.get("telefone_admin")
        usuario.cpf_admin = request.POST.get("cpf_admin")

        if funcionario:
            funcionario.nome = request.POST.get("nome")
            funcionario.cargo = request.POST.get("cargo")

        if imagem_form.is_valid():
            imagem_form.save()

        usuario.save()
        if funcionario:
            funcionario.save()

        return redirect("usuarios:perfil")

    else:
        imagem_form = ImagemPerfilForm(instance=usuario)

    return render(request, template, {
        "usuario": usuario,
        "funcionario": funcionario,
        "imagem_form": imagem_form,
    })



