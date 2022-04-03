from django.db import models
from django.contrib.auth.models import User

from location.models import Location

class FavoriteLocation(models.Model):
    user = models.ForeignKey(User, related_name='favorite_location', on_delete=models.CASCADE)
    location = models.ForeignKey(Location, related_name='favorite', on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-liked_at',]

    def __str__(self):
        return '%s' % self.id
# Create your models here.
