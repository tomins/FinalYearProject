from django.http import Http404
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import ParkingZone
from location.models import Location
from .serializers import ParkingZoneSerializer
import json
import logging
from django.http import HttpResponse
from math import radians, cos, sin, asin, sqrt



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
            address__contains = query
        )|Location.objects.get(
            name__contains = query
        )
        parkingZone = ParkingZone.objects.filter(
            postcode__contains = location.postcode,
        )
        #logging.info("line 28" + parkingZone[0]['name'])
        serializer = ParkingZoneSerializer(parkingZone, many = True)
        return serializer.data

#@api_view(['POST'])
def ParkingByDistance(request):
    logging.basicConfig(level=logging.INFO)
    query = request.data.get('query','')
    query = query.split(",",1)[0]
    logging.info("parking by distance: " + query)
    location = Location.objects.filter(address__contains = query)|Location.objects.filter(name__contains = query)
    logging.info("database name long: " + location.values('long')[0]['long'])
    logging.info("database name lat: " + location.values('lat')[0]['lat'])
    distance = request.data.get('distance','')
    
    longLoc = location.values('long')[0]['long']
    latLoc = location.values('lat')[0]['lat']
    parkingZone = ParkingZone.objects.all()
    parkingZoneFinal = []
    for p in parkingZone:
        latlongParkStr = p.latlong
        json_acceptable_string = latlongParkStr.replace("'", "\"")
        latLongJson = json.loads(json_acceptable_string)
        lat2 = latLongJson["lat"]
        long2 = latLongJson["lng"]
        d = checkDistance(distance, latLoc, longLoc, lat2, long2)
        setattr(p, 'distance', d)
        if(d<=float(distance)):
            parkingZoneFinal.append(p)
    serializer = ParkingZoneSerializer(parkingZoneFinal, many = True)
    return serializer.data

def checkDistance(distance, latLoc, longLoc, lat2, long2):
    long = radians(float(longLoc))
    long2 = radians(float(long2))
    lat = radians(float(latLoc))
    lat2 = radians(float(lat2))


    dlon = long2 - long
    dlat = lat2 - lat
    a = sin(dlat / 2)**2 + cos(lat) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))
    r = 3956 #radius of earth in miles
    d = (c * r)
    return d
    


@api_view(['POST'])
def ParkingDetail(request):
    logging.basicConfig(level=logging.INFO)
    query = request.data.get('query','')
    logging.info("88" + request.data.get('query',''))
    if query:
        try:
            parkingZone = ParkingZone.objects.filter(
                name__contains = query
            )
             
        except ParkingZone.DoesNotExist:
            return Http404
        serializer = ParkingZoneSerializer(parkingZone, many = True)
        return Response(serializer.data)
        