from django.contrib.auth.models import User, Group
from django.db import IntegrityError

from rest_framework import viewsets
from rest_framework.response import Response

from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.renderers import (
    BrowsableAPIRenderer,
    JSONRenderer
    )
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import mixins

from .serializers import (
    GroupSerializer,
    TrackSerializer,
    TrackPointSerializer,
    UserSerializer,
    FileSerializer,
    )
from .renderers import SVGRenderer
from .models import Track, TrackPoint
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


class TrackViewSet(
        mixins.ListModelMixin, mixins.RetrieveModelMixin,
        mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    API endpoint that allows tracks to be viewed or removed
    """
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, SVGRenderer, )


class TrackPointList(ListAPIView):
    """
    API endpoint that allows tracks to be viewed
    """
    serializer_class = TrackPointSerializer
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, SVGRenderer, )

    #make sure all points are displayed
    def paginate_queryset(self, queryset, view=None):
        return None

    def get_queryset(self):

        track_id = self.kwargs.get('track_id', None)

        if track_id is None:
            points = TrackPoint.objects.all()
        else:
            points = TrackPoint.objects.filter(track=track_id)

        return points

class FileUploadView(CreateAPIView):
    """
    API endpoint to upload gpx files
    """

    serializer_class = FileSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            try:
                SaveGPXtoModel(request.data['file'], request.user)
                return Response(status=201)
            except IntegrityError:
                return Response(
                    data={
                        'error': (
                            'IntegrityError, '
                            'This file is already in the database'
                            )
                        },
                    status=400
                )
        else:
            return Response(
                data=serializer.errors,
                status=400
            )
