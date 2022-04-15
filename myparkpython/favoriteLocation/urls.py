from django.urls import path, include
from favoriteLocation import views

urlpatterns = [
    path('get-favorite/', views.FavoriteList.as_view()),
    path('favoritelocation/new/', views.newFavorite),
    path('favoritelocation/delete/', views.deleteFavorite),
]
