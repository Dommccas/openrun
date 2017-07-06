from django.contrib.gis.db import models
from django.contrib.gis import admin as geoadmin
from django.contrib.auth.models import User
from django.template.defaultfilters import filesizeformat
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

import magic

from gpxpy import parser


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


@deconstructible
class FileValidator(object):
    error_messages = {
     'max_size': ("Ensure this file size is not greater than %(max_size)s."
                  " Your file size is %(size)s."),
     'min_size': ("Ensure this file size is not less than %(min_size)s. "
                  "Your file size is %(size)s."),
     'content_type': "Files of type %(content_type)s are not supported.",
     'invalid_gpx': "'%(file_name)s is not a valid gpx file'"
    }

    def __init__(self, max_size=None, min_size=None, content_types=()):
        self.max_size = max_size
        self.min_size = min_size
        self.content_types = content_types

    def __call__(self, data):
        if self.max_size is not None and data.size > self.max_size:
            params = {
                'max_size': filesizeformat(self.max_size),
                'size': filesizeformat(data.size),
            }

            raise ValidationError(
                self.error_messages['max_size'],
                'max_size', params
                )

        if self.min_size is not None and data.size < self.min_size:
            params = {
                'min_size': filesizeformat(self.min_size),
                'size': filesizeformat(data.size),
            }

            raise ValidationError(
                self.error_messages['min_size'],
                'min_size', params
                )

        if self.content_types:
            content_type = magic.from_buffer(data.read(), mime=True)
            data.seek(0)
            if content_type not in self.content_types:
                params = {'content_type': content_type}
                raise ValidationError(
                    self.error_messages['content_type'],
                    'content_type', params
                    )

    def __eq__(self, other):
        return isinstance(other, FileValidator)


class GPXFileValidator(FileValidator):
    def __call__(self, data):
        super(GPXFileValidator, self).__call__(data)

        try:
            parser.XMLParser(data.read().decode('ascii'))
            data.seek(0)
        except:
            params = {'file_name': data.filename}
            raise ValidationError(
                self.error_messages['invalid_gpx'],
                'invalid_gpx', params
                )


geoadmin.site.register(Track, geoadmin.OSMGeoAdmin)
