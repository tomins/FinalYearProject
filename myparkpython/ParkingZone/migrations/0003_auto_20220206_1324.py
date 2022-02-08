# Generated by Django 3.2.8 on 2022-02-06 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ParkingZone', '0002_rename_parkingarea_parkingzone'),
    ]

    operations = [
        migrations.AddField(
            model_name='parkingzone',
            name='disabledBays',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='parkingzone',
            name='evSpaces',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='parkingzone',
            name='height',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='parkingzone',
            name='numSpaces',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='parkingzone',
            name='openingHours',
            field=models.JSONField(default={}),
        ),
        migrations.AddField(
            model_name='parkingzone',
            name='rates',
            field=models.JSONField(default={}),
        ),
        migrations.AddField(
            model_name='parkingzone',
            name='security',
            field=models.JSONField(default={}),
        ),
        migrations.AddField(
            model_name='parkingzone',
            name='services',
            field=models.JSONField(default={}),
        ),
    ]