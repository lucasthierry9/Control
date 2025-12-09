from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return render(request, 'dashboard/index.html')
    else:
        return render(request, "control/index.html" )


