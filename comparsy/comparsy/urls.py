from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('website.urls')),       # normal pages
     # api pages   <-- add this
]
