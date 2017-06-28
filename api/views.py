from django.contrib.auth.models import User, Group

from rest_framework import viewsets

from . import serializers
from .models import Distance_Unit, Track


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = serializers.UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer


class DistanceUnitViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Distance_Unit.objects.all()
    serializer_class = serializers.DistanceUnitSerializer


class TrackViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tracks to be viewed or edited.
    """
    queryset = Track.objects.all()
    serializer_class = serializers.TrackSerializer
