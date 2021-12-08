from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Location
from .serializers import LocationSerializer

class LatestLocationList(APIView):
    def get(self,request,format=None):
        location = Location.objects.all()[0:1]
        serializer = LocationSerializer(location, many=True)
        return Response(serializer.data)




