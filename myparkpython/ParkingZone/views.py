from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import ParkingZone
from location.models import Location
from .serializers import ParkingZoneSerializer
import logging

class ParkingZoneList(APIView):
    def get(self, request, format=None):
        parkingZone = ParkingZone.objects.all()[0:5]
        serializer = ParkingZoneSerializer(parkingZone, many = True)
        return Response(serializer.data)

#@api_view(['POST'])
def ParkingZoneByLocation(request):
    logging.basicConfig(level=logging.INFO)
    query = request.data.get('query','')
    query = query.split(",",1)[0]
    if query:
        location = Location.objects.get(
            name__contains = query
        )
        parkingZone = ParkingZone.objects.filter(
            postcode__contains = location.postcode,
        )
        #logging.info("line 28" + parkingZone[0]['name'])
        serializer = ParkingZoneSerializer(parkingZone, many = True)
        return serializer.data