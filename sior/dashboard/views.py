from django.shortcuts import render
from django.shortcuts import redirect
from .models import Hat

# Create your views here.
def isauth(request):
    if request.user.is_authenticated:
        #print('auth')
        return redirect('../home')
    else:
        #print('no')
        return redirect('accounts/login')

def home(request):
    if not request.user.is_authenticated:
        return redirect('../accounts/login')
    else:
        return render(request, 'home.html', {})

def location(request):
    Hats = Hat.objects
    return render(request, 'location.html', {'Hats': Hats})


def statistics(request):
    return render(request, 'statistics.html', {})