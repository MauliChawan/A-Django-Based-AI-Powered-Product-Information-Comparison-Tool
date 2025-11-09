from django.shortcuts import render
from django.http import JsonResponse
from .models import Product
from django.contrib.auth import views as auth_views

def index(request):
    return render(request, 'base.html')

def loginPage(request):
    return render(request, 'login.html')

def signupPage(request):
    return render(request, 'signup.html')

def all_products(request):
    products = Product.objects.all().values()
    return JsonResponse(list(products), safe=False)

def comparePage(request):
    return render(request, 'website/compare.html')
