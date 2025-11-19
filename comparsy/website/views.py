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


# ----------------------------
# BASIC PAGES
# ----------------------------
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

        User.objects.create_user(
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



# -------------------------------------------------
# REAL-TIME AMAZON PRODUCT SEARCH - RAPIDAPI
# -------------------------------------------------
def api_search_products(request):
    query = request.GET.get("query", "").strip()

    if not query:
        return JsonResponse({"results": []})

    url = "https://real-time-amazon-data.p.rapidapi.com/search"
    params = {"query": query, "page": "1", "country": "IN"}

    headers = {
        "x-rapidapi-host": "real-time-amazon-data.p.rapidapi.com",
        "x-rapidapi-key": "7c7b9fd903mshe74fd83b4c1458fp159af5jsn249df19931e9",  # your key
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        data = response.json()

        # Expected location (correct)
        items = data.get("data", {}).get("products", [])

        # Normalize response
        clean = []
        for item in items:
            if not isinstance(item, dict):
                continue

            clean.append({
                "asin": item.get("asin") or "",
                "title": item.get("product_title") or "No Title",
                "price": item.get("product_price") or "0",
                "image": item.get("product_photo") or "",
                "rating": item.get("product_star_rating") or "0",
                "total_ratings": item.get("product_num_ratings") or "0",
                "specifications": item.get("product_details", {})
            })

        return JsonResponse({"results": clean})

    except Exception as e:
        print("API SEARCH ERROR:", e)
        return JsonResponse({
            "results": [],
            "error": "Search failed. Try again."
        }, status=502)



# -------------------------------------------------
# PRODUCT DETAILS API (optional)
# -------------------------------------------------
def api_product_details(request):
    asin = request.GET.get("asin", "").strip()

    if not asin:
        return JsonResponse({"error": "asin required"}, status=400)

    url = "https://real-time-amazon-data.p.rapidapi.com/product-details"

    headers = {
        "x-rapidapi-key": "7c7b9fd903mshe74fd83b4c1458fp159af5jsn249df19931e9",
        "x-rapidapi-host": "real-time-amazon-data.p.rapidapi.com"
    }

    params = {"asin": asin, "country": "IN"}

    try:
        r = requests.get(url, headers=headers, params=params, timeout=10)
        raw = r.json()
        return JsonResponse(raw)
    except Exception as e:
        return JsonResponse({
            "error": "Details API failed",
            "details": str(e)
        }, status=502)



# -------------------------------------------------
# SAVE COMPARISON (placeholder)
# -------------------------------------------------
@require_POST
@login_required
def api_save_comparison(request):
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except:
        return HttpResponseBadRequest("Invalid JSON")

    name = payload.get("name") or f"Comparison - {timezone.now()}"
    products = payload.get("products", [])

    return JsonResponse({
        "status": "ok",
        "name": name,
        "count": len(products)
    })


@login_required
def api_list_comparisons(request):
    return JsonResponse({
        "status": "pending",
        "message": "Comparison storage not implemented yet."
    })
