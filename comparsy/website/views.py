from django.shortcuts import render

def index(request):
    return render(request, 'base.html')

def loginPage(request):
    return render(request, 'login.html')

def signupPage(request):
    return render(request, 'signup.html')
