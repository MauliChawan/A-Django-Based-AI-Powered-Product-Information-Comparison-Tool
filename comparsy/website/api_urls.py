from django.urls import path
from . import views

urlpatterns = [
    # --- Product Search API ---
    path('search/', views.api_search_products, name='api_search'),

    # --- Product Details API ---
    path('product-details/', views.api_product_details, name='api_product_details'),

    # --- Comparison History APIs ---
    path("save-comparison/", views.api_save_comparison, name="api-save-comparison"),
    path("comparisons/", views.api_list_comparisons, name="api-list-comparisons"),
]
