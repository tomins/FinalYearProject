from rest_framework import serializers
from .models import FavoriteLocation
from location.serializers import LocationSerializer

class FavoriteLocationSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:

        model = FavoriteLocation
        fields = (
            "id",
            "email",
            "location"
        )