from django.shortcuts import render,redirect
from control.models import Usuario
from control.forms import UserForm

def cadastrar_usuario(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("usuarios:login")
    else:
        form = UserForm()
    return render(request, "registration/register.html", {"form": form})
# Create your views here.
