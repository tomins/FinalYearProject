from django.http import Http404
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import ParkingZone
from location.models import Location
from .serializers import ParkingZoneSerializer
import logging
from django.http import HttpResponse

class ParkingZoneList(APIView):
    def get(self, request, format=None):
        parkingZone = ParkingZone.objects.all()
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

@api_view(['POST'])
def ParkingByDistance(request):
    logging.basicConfig(level=logging.INFO)
    distance = request.data.get('distance','')
    lat = request.data.get('lat','')
    long = request.data.get('lat','')
    parkingZones = ParkingZone.objects.all()
    for ParkingZone in parkingZones:
        latlong = ParkingZone.latlong
        logging.info(latlong)
        lat2 = latlong[0]
        logging.info(lat2)
    return HttpResponse(status=200) 
    


@api_view(['POST'])
def ParkingDetail(request):
    logging.basicConfig(level=logging.INFO)
    query = request.data.get('query','')
    logging.info("line 28" + request.data.get('query',''))
    if query:
        try:
            parkingZone = ParkingZone.objects.filter(
                name__contains = query
            )
             
        except ParkingZone.DoesNotExist:
            return Http404
        serializer = ParkingZoneSerializer(parkingZone, many = True)
        return Response(serializer.data)
        