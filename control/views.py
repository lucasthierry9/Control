from django.shortcuts import render, redirect, get_object_or_404
from . models import Cliente
from . forms import ClienteForm
from django.contrib.auth.decorators import permission_required

# Create your views here.
def index(request):
    return render(request, "control/index.html" )


