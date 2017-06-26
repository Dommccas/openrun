from django.contrib.auth.models import User, Group

from rest_framework import serializers

from .models import Distance_Unit


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class DistanceUnitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Distance_Unit
        fields = ('url', 'name', 'suffix', 'conversion_factor')