from django.contrib.auth.models import User, Group
from django.conf import settings

from .models import Track, GPXFileValidator, TrackPoint

from rest_framework.serializers import (
    HyperlinkedModelSerializer,
    Serializer,
    FileField,
    )

from rest_framework_gis.serializers import GeoFeatureModelSerializer


class UserSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups', 'is_staff')


class GroupSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class TrackSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Track
        geo_field = 'track'
        fields = (
            'url', 'id', 'owner', 'file_hash', 'start', 'finish',
            'duration', 'distance', 'average_speed')


class TrackPointSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = TrackPoint
        geo_field = 'point'
        fields = (
             'id', 'point_type', 'time', 'elevation', 'track', 'segment_id',
             'speed')


class FileSerializer(Serializer):
    validate_file = GPXFileValidator(
        max_size=settings.DASHBOARD_UPLOAD_FILE_MAX_SIZE,
        content_types=settings.DASHBOARD_UPLOAD_FILE_TYPES
        )
    file = FileField(validators=[validate_file])
