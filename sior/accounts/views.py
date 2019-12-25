from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
# Create your views here.

def default(request):
    return redirect('login')

def login(request):
    if request.method == "POST":
        username = request.POST['InputID']
        password = request.POST['InputPassword']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            print('인증')
            return redirect('../../home')
        else:
            print('인증 실패')
            return render(request, 'login.html', {'error': 'username or password is incorrect'})
    else:
        return render(request, 'login.html', {})

def register(request):
    if request.method == "POST":
        if request.POST["InputPassword"] == request.POST["RepeatPassword"]:
            user = User.objects.create_user(
                username=request.POST["username"], password=request.POST["InputPassword"])
            auth.login(request, user)
            return redirect('../home')
    else:
        return render(request, 'register.html', {})

def logout(request):
    auth.logout(request)
    return redirect('../home')