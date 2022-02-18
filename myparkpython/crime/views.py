from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Crime
import requests
from .serializer import CrimeSerializer
import logging

@api_view(['POST'])
def search(request):
    logging.basicConfig(level=logging.INFO)
    name = request.data.get('name','')
    latlng = request.data.get('latlng','')
    r = requests.get('http://')
