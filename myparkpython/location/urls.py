from django.urls import path, include
from location import views

urlpatterns = [
    path('latest-location/', views.LatestLocationList.as_view()),
    path('location/search/', views.search),
]
