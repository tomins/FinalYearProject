from django.db import models
from django.forms import FloatField, IntegerField, JSONField

class ParkingZone(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    rates = JSONField()
    openingHours = JSONField()
    services = JSONField()
    security = JSONField()
    numSpaces = IntegerField()
    evSpaces = IntegerField()
    height = FloatField()
    disabledBays = IntegerField()
    postcode = models.CharField(max_length=7)

    class Meta:
        ordering = ('postcode',)

    def __str__(self):
        return self.name + self.address + self.rates + self.openingHours + self.services + self.security + self.numSpaces + self.evSpaces + self.height + self.disabledBays

    
