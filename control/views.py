from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    return render(request, 'control/index.html')


