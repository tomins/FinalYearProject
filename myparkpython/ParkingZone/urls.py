from django.urls import path, include
from ParkingZone import views

urlpatterns = [
    path('ParkingZoneList/', views.ParkingZoneList.as_view()),
    path('ParkingZoneByLocation/', views.ParkingZoneByLocation),
]