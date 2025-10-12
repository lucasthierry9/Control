from django.shortcuts import render, redirect, get_object_or_404
from . models import Cliente
from . forms import ClienteForm

# Create your views here.
def index(request):
    return render(request, "control/index.html" )

def login(request):
    return render(request, "control/login.html")

