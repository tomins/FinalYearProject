# Generated by Django 3.2.8 on 2022-03-07 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ParkingZone', '0006_parkingzone_latlong'),
    ]

    operations = [
        migrations.AddField(
            model_name='parkingzone',
            name='distance',
            field=models.FloatField(default=0),
        ),
    ]