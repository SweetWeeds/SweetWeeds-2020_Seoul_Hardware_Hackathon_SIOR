from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.
def isauth(request):
    if request.user.is_authenticated:
        #print('auth')
        return redirect('home')
    else:
        #print('no')
        return redirect('accounts/login')

def home(request):
    if not request.user.is_authenticated:
        return redirect('../accounts/login')
    else:
        return render(request, 'home.html', {})

def location(request):
    return render(request, 'location.html', {})