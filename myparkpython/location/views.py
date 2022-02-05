from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import re
import ParkingZone

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
        getParkingZoneQ()
        return Response(serializer.data)

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

    for x in p:
        x = "https://www.q-park.co.uk" + x #this makes x a full link not just partial
        req = requests.get(x)
        s = BeautifulSoup(req.text, 'html.parser')

        #name, address and postcode
        for y in s.find_all('div',"card-meta-information parkingDetailCard-meta"):
            for n  in y.find_all('strong'):
                nameA = n.get_text(strip=True)#Strip means take away all whitespace at start and end of the string"
            addressA = addressA + y.get_text(strip=True)
        postcode = addressA.split("london",1)[1]
        postcode = postcode.split(" ")[0]
        #end name, address and postcode

        #rates
        for t in s.find_all('div',"tariff-content-row"):
            for n in t.find_all('span',"grey"):
                ratesA["hours"] = n.get_text(strip = True)
            for n in t.find_all('span',"large-text"):
                ratesA["cost"] = n.get_text(strip=True)
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
                numSpacesA = n.get_text(strip = True)
            for n in t.find_all(attrs={"data-notice":"Blue badge parking spaces"}):
                disabledBaysA = n.get_text(strip = True)
            for n in t.find_all(attrs={"data-notice":"EV charging parking spaces"}):
                evSpacesA = n.get_text(strip = True)
            for n in t.find_all(attrs={"data-notice":"Max. height"}):
                heightA = n.get_text(strip = True)
        #end spaces, disabledBays, ev, height

        #now to create instance of model and put into db
        park = ParkingZone(
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
            postcode = postcodeA
        )
        park.save()
        #end creating and saving parking zone, also end for loop for each parking area
    #after for loop through all pages ends
#after def
        



