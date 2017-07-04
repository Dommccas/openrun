from django.contrib.auth.models import User, Group

from rest_framework import viewsets, views
from rest_framework.response import Response

from rest_framework.renderers import (
    BrowsableAPIRenderer,
    JSONRenderer
    )

from rest_framework.parsers import FileUploadParser
from rest_framework import mixins
from rest_framework import generics

from .serializers import (
    DistanceUnitSerializer,
    GroupSerializer,
    TrackSerializer,
    UserSerializer,
    FileUploadSerializer,
    )

from .renderers import SVGRenderer
from .models import Distance_Unit, Track
from .utils import SaveGPXtoModel


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


class TrackViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """
    API endpoint that allows tracks to be viewed or removed
    """
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, SVGRenderer, )


class FileUploadView(generics.CreateAPIView):
    """
    API endpoint to upload gpx files
    """

    serializer_class = FileUploadSerializer
    parser_classes = (FileUploadParser, )

    def create(self, request, filename):

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            SaveGPXtoModel(request.data['file'], request.user)
            return Response(status=201)
        else:
            return Response(status=400)



