from django.shortcuts import render,redirect
from usuarios.models import Usuario
from usuarios.forms import UserForm

def cadastrar_usuario(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("usuarios:login")
    else:
        form = UserForm()
    return render(request, "registration/register.html", {"form": form})

