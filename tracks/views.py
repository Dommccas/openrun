from django.contrib.auth.models import User, Group

from rest_framework import viewsets

from .serializers import UserSerializer, GroupSerializer, DistanceUnitSerializer
from .models import Distance_Unit


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class DistanceUnitViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Distance_Unit.objects.all()
    serializer_class = DistanceUnitSerializer