from django.urls import path
from .views import fetch_comments, health_check

urlpatterns = [
    path('health/', health_check, name='health-check'),
    path('fetch-comments/', fetch_comments, name='fetch-comments'),
]
