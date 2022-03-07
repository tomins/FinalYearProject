from email.policy import default
from django.db import models


class ParkingZone(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    postcode = models.CharField(max_length=10)
    rates = models.JSONField(default=[])
    openingHours = models.JSONField(default=[])
    services = models.JSONField(default=[])
    security = models.JSONField(default=[])
    numSpaces = models.IntegerField(default=0)
    evSpaces = models.IntegerField(default=0)
    height = models.FloatField(default=0)
    disabledBays = models.IntegerField(default=0)
    latlong = models.CharField(max_length=50)
    distance = models.FloatField(default=0)
    
    class Meta:
        ordering = ('postcode',)

    def __str__(self):
        return self.name

    
