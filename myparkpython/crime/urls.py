from django.urls import path, include
from crime import views

urlpatterns = [
    path('crime/search/', views.search),
]