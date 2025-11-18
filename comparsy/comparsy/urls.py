# File location: comparsy/urls.py (Example)

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # INCLUDE THE WEBSITE APP'S GENERAL URLS (index, login, etc.)
    # This assumes your app is named 'website'
    path('', include('website.urls')), 
    
    # 💥 CRUCIAL FIX: INCLUDE THE API ROUTES WITH THE '/api/' PREFIX 💥
    # This line tells Django that all paths defined in 'website/api_urls.py'
    # must be prefixed with '/api/'.
    path('api/', include('website.api_urls')), 
]