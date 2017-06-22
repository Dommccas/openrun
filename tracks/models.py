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
        return self.start.strftime("%a %p %-d %B %Y")

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


class Point(models.Model):
    POINT_TYPES = (
        ('S', 'Start'),
        ('F', 'Finish'),
        ('P', 'Pause'),
        ('R', 'Resume'),
        ('A', 'Active'),
        )

    point_type = models.CharField(max_length=1, choices=POINT_TYPES)
    time = models.DateTimeField()
    elevation = models.DecimalField(max_digits=7, decimal_places=2)
    gpx_track = models.ForeignKey(Track)
    point = models.PointField()
    objects = models.GeoManager()

    def __str__(self):
        return self.gpx_track.start.strftime("%a %p %-d %B %Y") \
            + ': ' \
            + self.point_type


class Distance_Unit(models.Model):
    name = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        unique=True)
    suffix = models.CharField(
        max_length=2,
        null=False,
        blank=False,
        unique=True)
    conversion_factor = models.DecimalField(
        "conversion factor from kilometers",
        blank=True,
        null=True,
        max_digits=10,
        decimal_places=7)
    objects = models.Manager

    def __str__(self):
        return self.name


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    distance_unit = models.ForeignKey(Distance_Unit, null=True, blank=True)
    pace = models.BooleanField(default=True)

    def pace_string(self):
        if self.pace:
            return 'minute ' + self.distance_unit.name
        else:
            return self.distance_unit.suffix + '/hour'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


geoadmin.site.register(Point, geoadmin.OSMGeoAdmin)
geoadmin.site.register(Track, geoadmin.OSMGeoAdmin)
geoadmin.site.register(Distance_Unit, geoadmin.OSMGeoAdmin)
geoadmin.site.register(Profile, geoadmin.OSMGeoAdmin)
