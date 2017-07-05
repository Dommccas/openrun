from django.contrib.gis.db import models
from django.contrib.gis import admin as geoadmin
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Track(models.Model):

    class Meta:
        ordering = ['-start']

    track = models.MultiLineStringField()
    owner = models.ForeignKey(User)
    file_hash = models.CharField("md5 hash value", max_length=32, unique=True)
    start = models.DateTimeField("start date and time", blank=True, null=True)
    finish = models.DateTimeField(
        "finish date and time", blank=True, null=True)
    duration = models.DecimalField(
        "total moving time in hours", blank=True,
        null=True, max_digits=10, decimal_places=2)
    distance = models.DecimalField(
        "total moving distance in kilometers", blank=True,
        null=True, max_digits=7, decimal_places=2)
    average_speed = models.DecimalField(
        "average moving speed in kilometers per hour",
        blank=True, null=True, max_digits=7, decimal_places=2)
    objects = models.GeoManager()

    def __str__(self):
        return self.file_hash

    def distance_user_units(self):
        return round(
            self.distance * self.owner.profile.distance_unit.conversion_factor,
            2)

    def speed_user_units(self):
        pace_conversion_factor = 60 if self.owner.profile.pace else 1
        return round(
            pace_conversion_factor / (
                self.average_speed
                * self.owner.profile.distance_unit.conversion_factor
                ),
            2)


geoadmin.site.register(Track, geoadmin.OSMGeoAdmin)

