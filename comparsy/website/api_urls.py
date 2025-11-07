from django.urls import path
from .views import all_products


urlpatterns = [
    path('all-products/', all_products, name="all_products_api"),
]

