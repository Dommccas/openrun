from django.contrib.auth.models import User, Group

from .models import Distance_Unit, Track

from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups', 'is_staff')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class DistanceUnitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Distance_Unit
        fields = ('url', 'name', 'suffix', 'conversion_factor')


class TrackSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Track
        geo_field = 'track'
        id_field = False
        fields = (
            'owner', 'file_hash', 'start', 'finish',
            'duration', 'distance', 'average_speed')


