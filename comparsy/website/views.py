import os
import json
import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.conf import settings
# ---------------------------------------
# RapidAPI Credentials (stored in env)
# ---------------------------------------
RAPIDAPI_KEY = settings.RAPIDAPI_KEY
RAPIDAPI_HOST = settings.RAPIDAPI_HOST


# ---------------------------------------
# BASIC PAGES
# ---------------------------------------
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

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=fullname
        )

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


def comparePage(request):
    return render(request, "website/compare.html")


# ---------------------------------------
# AMAZON SEARCH (RapidAPI)
# ---------------------------------------
def api_search_products(request):
    """
    GET /api/search/?query=iphone
    Returns a CLEAN products list used by frontend.
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
        "country": "US",
        "sort_by": "RELEVANCE"
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        # Raises HTTPError for 4xx or 5xx responses (e.g., 403 for bad key)
        response.raise_for_status() 
        raw = response.json()
    except Exception as e:
        # Returns 502 if the Upstream API (RapidAPI) fails
        return JsonResponse({
            "error": "Upstream API failed",
            "details": str(e)
        }, status=502)

    products = []
    # Note: If the response structure changes, this parsing loop may need adjustment
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

    # Returns the list under the "results" key expected by search.js
    return JsonResponse({"results": products})


# ---------------------------------------
# AMAZON PRODUCT DETAILS
# ---------------------------------------
def api_product_details(request):
    """
    GET /api/product-details/?asin=B0CMZ8ZBVN
    """
    asin = request.GET.get("asin", "").strip()

    if not asin:
        return JsonResponse({"error": "asin parameter required"}, status=400)

    if not RAPIDAPI_KEY:
        return JsonResponse({"error": "Missing RAPIDAPI_KEY"}, status=500)

    url = f"https://{RAPIDAPI_HOST}/product-details"

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }

    params = {
        "asin": asin,
        "country": "IN"
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        raw = response.json()
    except Exception as e:
        return JsonResponse({
            "error": "Upstream API failed",
            "details": str(e)
        }, status=502)

    # Returns the raw API response for the frontend to process details
    return JsonResponse(raw)


# ---------------------------------------
# SAVE COMPARISON HISTORY (Placeholders)
# ---------------------------------------
@require_POST
@login_required
def api_save_comparison(request):
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except:
        return HttpResponseBadRequest("Invalid JSON")

    name = payload.get("name") or f"Comparison - {timezone.now().strftime('%Y-%m-%d %H:%M')}"
    products = payload.get("products", [])

    # TODO: Save in DB once Comparison model is created
    return JsonResponse({
        "status": "ok",
        "saved": True,
        "name": name,
        "count": len(products)
    })


@login_required
def api_list_comparisons(request):
    return JsonResponse({
        "status": "not_implemented",
        "message": "Create a Comparison model to store history."
    })