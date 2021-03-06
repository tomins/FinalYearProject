from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    lat = models.CharField(max_length=30)
    long = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    postcode = models.CharField(max_length=10)

    class Meta:
        ordering = ('name',)

    def __str___(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}/'


