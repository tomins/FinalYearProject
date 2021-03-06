from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404
from location.models import Location

from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse

from .models import FavoriteLocation
from .serializers import FavoriteLocationSerializer
import logging

class FavoriteList(APIView):
    logging.basicConfig(level=logging.INFO)
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        favoriteLocations = FavoriteLocation.objects.filter(user=request.user)
        #logging.info("get in favorite location: " + favoriteLocations[0].location.name)
        serializer = FavoriteLocationSerializer(favoriteLocations, many=True)
        return Response(serializer.data)
# Create your views here.

@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def newFavorite(request):
    logging.basicConfig(level=logging.INFO)
    query = request.data.get('query','')
    q2 = query.split(",",1)[0]
    logging.info("new Favorite: " + q2)
    if query:
        try:
            loc = Location.objects.get(
                address__contains = q2
            )
        except Location.DoesNotExist:
            loc = Location.objects.get(
                name__contains = q2
            )
        #if(loc.count() >0):
        #logging.info("the location has been found: " + loc['name'])
        obj, park = FavoriteLocation.objects.get_or_create(
            user = request.user,
            location = loc)
        return HttpResponse(status=200)
        


@api_view(['PUT'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def deleteFavorite(request):
    logging.basicConfig(level=logging.INFO)
    query = request.data.get('query','')
    query = query.split(",",1)[0]
    logging.info("delete favorite: " + query)
    if query:
        location = Location.objects.get(
            name__contains = query
        )
    park = FavoriteLocation.objects.get(
        user = request.user,
        location = location)
    park.delete()
    return HttpResponse(status=200)