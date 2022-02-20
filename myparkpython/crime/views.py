from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Crime
import requests
from .serializer import CrimeSerializer
import logging
from django.http import HttpResponse
import json
from math import radians, cos, sin, asin, sqrt

@api_view(['POST'])
def search(request):
    logging.basicConfig(level=logging.INFO)
    name = request.data.get('name','')
    name = name["address"]
    latlng = request.data.get('latlng','')
    latlng =latlng.replace("(","")
    latlng =latlng.replace(")","")
    lat = latlng.split(',')[0]
    long = latlng.split(',')[1]
    long = long.strip()
    #add a get or create here

    r = requests.get('https://data.police.uk/api/crimes-street/vehicle-crime?lat=' + lat + '&lng=' + long)
    j = json.loads(r.text)#list
    num_crimes = 0
    for d in j:#dict
        lat2 = d["location"]['latitude']
        long2 = d["location"]['longitude']
        if(distance(lat,lat2,long,long2)<0.2):
            num_crimes = num_crimes +1
        
    obj, crime = Crime.objects.get_or_create(
            name = name,
            num_crimes = num_crimes
        )
    
    serializer = CrimeSerializer(obj)
    return Response(serializer.data)

def distance(lat,lat2,long,long2):
    long = radians(float(long))
    long2 = radians(float(long2))
    lat = radians(float(lat))
    lat2 = radians(float(lat2))

    dlon = long2 - long
    dlat = lat2 - lat
    a = sin(dlat / 2)**2 + cos(lat) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))
    r = 3956 #radius of earth in miles
    return(c * r)
