# Generated by Django 3.2.8 on 2022-02-07 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='address',
            field=models.CharField(default=[], max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='location',
            name='postcode',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
    ]
