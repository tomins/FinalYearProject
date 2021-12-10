from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Location
from .serializers import LocationSerializer

class LatestLocationList(APIView):
    def get(self,request,format=None):
        location = Location.objects.all()[0:1]
        serializer = LocationSerializer(location, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def search(request):
    query = request.data.get('query','')

    if query:
        location = Location.objects.all()[0:1]
        serializer = LocationSerializer(location, many=True)
        return Response(serializer.data)



