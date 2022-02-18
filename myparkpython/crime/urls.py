from django.urls import path, include
from crime import views

urlpatterns = [
    path('search/', views.search),
]