# views.py
import os
import requests
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.http import require_POST

# If you create a Comparison model (recommended) put it in models.py and import here:
# from .models import Comparison

# ---------- Helper: read RapidAPI credentials from environment ----------
RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY")        # set this in your env (never commit)
RAPIDAPI_HOST = os.environ.get("RAPIDAPI_HOST", "real-time-amazon-data.p.rapidapi.com")


# ---------- Page views (signup/login/index) ----------
def index(request):
    return render(request, "base.html")


def signupPage(request):
    if request.method == "POST":
        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not (fullname and email and password):
            messages.error(request, "Please fill all fields.")
            return redirect("signup")

        if User.objects.filter(username=email).exists():
            messages.error(request, "This email is already registered.")
            return redirect("signup")

        user = User.objects.create_user(username=email, email=email, password=password, first_name=fullname)
        messages.success(request, "Account created successfully. Please login.")
        return redirect("login")

    return render(request, "signup.html")


def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, "Invalid username or password.")
            return redirect("login")
        login(request, user)
        messages.success(request, "Logged in successfully.")
        return redirect("index")

    return render(request, "login.html")


# ---------- API: Search Amazon products (via RapidAPI) ----------
def api_search_products(request):
    """
    GET /api/search/?query=iphone 15
    Returns a cleaned list of search results from the RapidAPI Amazon search endpoint.
    """
    query = request.GET.get("query", "").strip()
    if not query:
        return JsonResponse({"error": "query parameter required"}, status=400)

    if not RAPIDAPI_KEY:
        return JsonResponse({"error": "Missing RAPIDAPI_KEY on server"}, status=500)

    url = f"https://{RAPIDAPI_HOST}/search"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }
    params = {
        "query": query,
        "page": 1,
        "country": "US",   # change as needed or accept from client
        "sort_by": "RELEVANCE"
    }

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        resp.raise_for_status()
        raw = resp.json()
    except Exception as e:
        return JsonResponse({"error": "Upstream API request failed", "details": str(e)}, status=502)

    # The returned structure from your sample:
    # { "status": "...", "data": { "products": [ {asin, product_title, product_price, ...}, ... ] } }
    products = []
    for p in raw.get("data", {}).get("products", [])[:20]:
        products.append({
            "asin": p.get("asin"),
            "title": p.get("product_title"),
            "price": p.get("product_price"),
            "original_price": p.get("product_original_price"),
            "rating": p.get("product_star_rating"),
            "total_ratings": p.get("product_num_ratings"),
            "image": p.get("product_photo"),
            "url": p.get("product_url"),
        })

    return JsonResponse({"results": products})


# ---------- API: Product details (by ASIN) ----------
def api_product_details(request):
    """
    GET /api/product-details/?asin=B0CMZ8ZBVN
    Returns full product details for a single ASIN from RapidAPI.
    """
    asin = request.GET.get("asin", "").strip()
    if not asin:
        return JsonResponse({"error": "asin parameter required"}, status=400)

    if not RAPIDAPI_KEY:
        return JsonResponse({"error": "Missing RAPIDAPI_KEY on server"}, status=500)

    url = f"https://{RAPIDAPI_HOST}/product-details"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }
    params = {
        "asin": asin,
        "country": "US"
    }

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        resp.raise_for_status()
        raw = resp.json()
    except Exception as e:
        return JsonResponse({"error": "Upstream API request failed", "details": str(e)}, status=502)

    # Return raw to frontend (or you can normalize specific fields)
    return JsonResponse(raw)


# ---------- History endpoints (store only comparisons) ----------
# NOTE: you need a Comparison model. Example model suggested below in notes.
@require_POST
@login_required
def api_save_comparison(request):
    """
    POST JSON body:
    {
      "name": "Comparison - Nov 15",
      "products": [ {asin: "...", title: "...", price: "...", specs: {...} }, ... ]
    }
    """
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return HttpResponseBadRequest("Invalid JSON")

    name = payload.get("name") or f"Comparison - {timezone.now().strftime('%Y-%m-%d %H:%M')}"
    products = payload.get("products", [])

    # if you created a Comparison model:
    # comp = Comparison.objects.create(user=request.user, name=name, products=products)
    # return JsonResponse({"id": comp.id, "name": comp.name, "created_at": comp.created_at.isoformat()})

    # Fallback: if no model, just echo back (you should create model & uncomment above)
    return JsonResponse({"status": "ok", "name": name, "num_products": len(products)})


@login_required
def api_list_comparisons(request):
    """
    Return saved comparisons for the logged-in user.
    If you implement a Comparison model, query and return them here.
    """
    # If you have Comparison model, do:
    # comps = Comparison.objects.filter(user=request.user).order_by("-created_at")
    # return JsonResponse([...], safe=False)

    return JsonResponse({"status": "not_implemented", "message": "Create a Comparison model and update this view."})


# ---------- Optional: product compare page ----------
def comparePage(request):
    # This template will render your 3-box UI + the area where JS will populate cards + table
    return render(request, "website/compare.html")
import requests
from django.http import JsonResponse

def search_amazon_products(request):
    query = request.GET.get("query", "")

    if not query:
        return JsonResponse({"error": "Missing search query"}, status=400)

    url = "https://real-time-amazon-data.p.rapidapi.com/search"
    params = {
        "query": query,
        "page": "1",
        "country": "IN"
    }

    headers = {
        "x-rapidapi-key": "7c7b9fd903mshe74fd83b4c1458fp159af5jsn249df19931e9",
        "x-rapidapi-host": "real-time-amazon-data.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        return JsonResponse(data, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
