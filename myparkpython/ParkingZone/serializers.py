from rest_framework import serializers
from .models import ParkingZone

class ParkingZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingZone
        fields = (
            "name",
            "address",
            "rates",
            "openingHours",
            "services",
            "security",
            "numSpaces",
            "evSpaces",
            "height",
            "disabledBays",
            "postcode",
            "latlong"
        )
