from django.urls import path
from . import views

urlpatterns = [
    path("search/", views.api_search_products, name="api_search"),
    path("product-details/", views.api_product_details, name="api_product_details"),

    # Comparison History APIs
    path("save-comparison/", views.api_save_comparison, name="api-save-comparison"),
    path("comparisons/", views.api_list_comparisons, name="api-list-comparisons"),
]
