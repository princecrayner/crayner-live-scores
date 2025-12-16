from django.contrib import admin
from django.urls import path, include
from api.views import live_page

urlpatterns = [
    path('', live_page),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
