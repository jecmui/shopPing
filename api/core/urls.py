from django.contrib import admin
from django.urls import path, include
from core.health.views import health_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_view, name='health'),
]
