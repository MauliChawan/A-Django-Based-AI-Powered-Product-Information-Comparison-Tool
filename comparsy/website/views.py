from django.shortcuts import render
from django.http import JsonResponse
from .models import Product

def index(request):
    return render(request, 'base.html')

def loginPage(request):
    return render(request, 'login.html')

def signupPage(request):
    return render(request, 'signup.html')

def all_products(request):
    products = Product.objects.all().values()
    return JsonResponse(list(products), safe=False)
