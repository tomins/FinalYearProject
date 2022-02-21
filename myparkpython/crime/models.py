from django.db import models

# Create your models here.

class Crime(models.Model):
    name = models.CharField(max_length=100)
    num_crimes = models.CharField(max_length=100)

    class Meta:
        ordering = ('name',)

    def __str___(self):
        return self.name
