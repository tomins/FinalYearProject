from ast import Str
from http.client import ImproperConnectionState
from urllib import request
from django.shortcuts import render
import requests
from ParkingZone.views import ParkingZoneByLocation
from ParkingZone.views import ParkingByDistance
from bs4 import BeautifulSoup
import re
from ParkingZone.models import ParkingZone
from django.db import models
import json
import urllib
from django.http import HttpResponse
from django.http import Http404
import logging

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
def create(request):
    logging.basicConfig(level=logging.INFO)
    r = request.data.get('address','')
    soup= BeautifulSoup(r, 'html.parser')
    name = request.data.get('name','')

    
    location = Location.objects.filter(
            address__contains = name
        )|Location.objects.filter(
            name__contains = name
        )
    if(location.count() >0):
        #logging.info("the location has been found: " + location['name'])
        return HttpResponse(status=200)
    
    else:
        logging.info("name: " + name)
        address = ""
        for x in soup.find_all('span',"street-address"):
            address = address + x.text + ","
        #logging.info(address)
        lat = request.data.get('lat','')
        long = request.data.get('long','')
        p = []
        for x in soup.find_all('span',"postal-code"):
            p.append(x.text)
        postcode = p[0]
        postcode = postcode.split(" ",1)[0]
        
        #logging.info(postcode)

        if name:
            obj, location = Location.objects.get_or_create(
                name = name,
                lat = lat,
                long = long,
                address = address,
                postcode = postcode
            )
            logging.info(obj)
            serializer = LocationSerializer(obj)
            return Response(serializer.data)
        
        
    

@api_view(['POST'])
def search(request):
    logging.basicConfig(level=logging.INFO)
    query = request.data.get('query','')
    query = query.split(",",1)[0]
    logging.info("search: " + query)
    if query:
        location = Location.objects.filter(
            name__contains = query
        )|Location.objects.filter(
            address__contains = query
        )
        #logging.info("size: " + str(location.count()))
        getParkingZoneQ() 
        return Response(ParkingByDistance(request))

def getParkingZoneQ():
    r = requests.get('https://www.q-park.co.uk/en-gb/cities/london/')
    soup = BeautifulSoup(r.text, 'html.parser')
    parking = []
    for x in soup.find_all('section',"list-all city-parking"):
        parking.append(x)
    parkingLinks = []
    for x in parking:
        for link in x.find_all(href=re.compile("london")):
            parkingLinks.append(link.get('href'))

    p = []
    for x in parkingLinks:
        if "poi" in x:
            parkingLinks.remove(x)#not fully working
        else:
            p.append(x)#hence new variable

    #This ends getting the list of links for each parking area, so now going to go through each one and add it to a model

    ##now create all variables needed
    

    for x in p:
        nameA = ""
        addressA =""
        ratesA = {}
        openingHoursA = {}
        servicesA = []
        securityA = []
        numSpacesA = 0
        heightA = 0 
        evSpacesA = 0
        disabledBaysA = 0
        postcodeA = ""
        latlong = ""
        x = "https://www.q-park.co.uk" + x #this makes x a full link not just partial
        req = requests.get(x)
        s = BeautifulSoup(req.text, 'html.parser')

        #name, address and postcode
        for y in s.find_all('div',"card-meta-information parkingDetailCard-meta"):
            for n  in y.find_all('strong'):
                nameA = n.get_text(strip=True) + " " #Strip means take away all whitespace at start and end of the string"
            addressA = addressA +  y.get_text(strip=True) + " " 


        try:
            parkingzone = ParkingZone.objects.filter(
                address__contains = nameA
            )|ParkingZone.objects.filter(
                name__contains = nameA
            )
            if(parkingzone.count() >0):
                logging.info("the location has been found: " + nameA)
                return HttpResponse(status=200)
        except Location.DoesNotExist:    
            postcodeA = addressA.split("London",1)[1]
            postcodeA = postcodeA.split(" ",2)[1]
            latlong = doLatLong(nameA)
            #end name, address and postcode

            #rates
            ratehours = []
            ratecost = []
            for t in s.find_all('div',"tariff-content-row"):
                for n in t.find_all('span',"grey"):
                    ratehours.append(n.get_text(strip = True))
                for n in t.find_all('span',"large-text"):
                    ratecost.append(n.get_text(strip=True))
            ratesA["hours"] = ratehours
            ratesA["cost"] = ratecost
            #end rates

            #opening hours
            for t in s.find_all('div',"open-hours-row"):
                for x in t.find_all('span',"label"):
                    openingHoursA["days"] = x.get_text(strip=True)
                for x in t.find_all('span',"entry"):
                    openingHoursA["entry"] = x.get_text(strip=True)
                for x in t.find_all('span',"exit"):
                    openingHoursA["exit"] = x.get_text(strip=True)
            #end opening hours

            #services
            for t in s.find_all('div',"row row-no-gutters services-content"):
                for d in t.find_all('div'):
                    servicesA.append(d.get_text(strip=True))
            #end services

            #security
            for t in servicesA:
                if "CCTV in operation" in t:
                    securityA.append(t)
            #end security

            #spaces, disabledBays, ev, height
            for t in s.find_all('div',"facility-card-element"):
                for n in t.find_all(attrs={"data-notice":"Standard parking spaces"}):
                    numSpacesA = t.get_text(strip=True)
                for n in t.find_all(attrs={"data-notice":"Blue badge parking spaces"}):
                    disabledBaysA = t.get_text(strip=True)
                for n in t.find_all(attrs={"data-notice":"EV charging parking spaces"}):
                    evSpacesA =t.get_text(strip=True)
                for n in t.find_all(attrs={"data-notice":"Max. height"}):
                    heightA = t.get_text(strip=True)
            #end spaces, disabledBays, ev, height

            #now to create instance of model and put into db
            obj, park = ParkingZone.objects.get_or_create(
                name = nameA,
                address = addressA,
                rates = {
                    'hours' : ratesA["hours"],
                    'price' : ratesA["cost"],
                },
                openingHours = {
                    'days': openingHoursA["days"],
                    'entry' : openingHoursA["entry"],
                    'exit' : openingHoursA["exit"],
                },
                services = {
                    'list' : [servicesA],
                },
                security = {
                    'list': [securityA],
                },
                numSpaces = numSpacesA,
                disabledBays = disabledBaysA,
                evSpaces = evSpacesA,
                height = heightA,
                postcode = postcodeA,
                latlong = latlong
            )
        
        #end creating and saving parking zone, also end for loop for each parking area
    #after for loop through all pages ends
#after def

def doLatLong(nameA):
    logging.basicConfig(level=logging.INFO)
    base_url= "https://maps.googleapis.com/maps/api/geocode/json?"
    AUTH_KEY = "AIzaSyDWmiNZ5XRvjoGggjfUP-_FGj8cycVu1LE"
    parameters = {"address": nameA, "key": AUTH_KEY}
    r = requests.get(f"{base_url}{urllib.parse.urlencode(parameters)}") 
    data = json.loads(r.content)
    return data.get("results")[0].get("geometry").get("location")

@api_view(['POST'])
def getLocation(request):
    logging.basicConfig(level=logging.INFO)
    query = request.data.get('query','')
    query = query.split(",",1)[0]
    
    if query:
        try:
            location = Location.objects.filter(
                address__contains = query
            )|Location.objects.filter(
                name__contains = query
            )
            
             
        except Location.DoesNotExist:
            return Http404
        serializer = LocationSerializer(location, many = True)
        return Response(serializer.data)


