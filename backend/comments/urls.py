from django.urls import path
from .views import fetch_comments

urlpatterns = [
    path('fetch-comments/', fetch_comments, name='fetch-comments'),
]
