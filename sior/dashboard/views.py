from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        print('auth')
        return redirect('index')
    else:
        print('no')
        return redirect('accounts/login')
    return redirect('index')