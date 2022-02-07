from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import ParkingZone
from .serializers import ParkingZoneSerializer

class ParkingZoneList(APIView):
    def get(self, request, format=None):
        parkingZone = ParkingZone.objects.all()[0:5]
        serializer = ParkingZoneSerializer(parkingZone, many = True)
        return Response(serializer.data)

@api_view(['POST'])
def ParkingZoneByLocation(request):
    location = request.data.get('query','')
    if location:
        parkingZone = ParkingZone.objects.filter(
            postcode = location.postcode,
        )
        serializer = ParkingZoneSerializer(parkingZone, many = True)
        return Response(serializer.data)