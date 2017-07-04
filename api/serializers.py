from django.contrib.auth.models import User, Group
from django.conf import settings
from django.template.defaultfilters import filesizeformat
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import Distance_Unit, Track
from .utils import GenerateFileHash

from rest_framework.serializers import (
    HyperlinkedModelSerializer,
    ModelSerializer,
    )

from rest_framework_gis.serializers import GeoFeatureModelSerializer

from gpxpy import parser

class UserSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups', 'is_staff')


class GroupSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class DistanceUnitSerializer(HyperlinkedModelSerializer):
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


class FileUploadSerializer(ModelSerializer):
    class Meta:
        model = Track
        fields = (
            'owner', 'file_hash', 'start', 'finish',
            'duration', 'distance', 'average_speed')

    def validate(self, validated_data):

        file_errors=[]

        f = self.data['file']

        # check file has only one full stop in it.
        if len(f.name.split('.')) != 2:
            file_errors.append(ValidationError(
                _('%(file_name)s has not been uploaded: '\
                'File type is not supported'),
                params={'file_name': f.name},
                code='file_type')
                )

        # check file doesn't breach the file size listed in settings
        if f.content_type in settings.DASHBOARD_UPLOAD_FILE_TYPES:
            if f._size > settings.DASHBOARD_UPLOAD_FILE_MAX_SIZE:
                file_errors.append(ValidationError(
                    _('%(file_name)s has not been uploaded: File too '\
                    'big. Please keep filesize under %(setting_size)s. '\
                    'Current filesize %(file_size)s'),
                    params={
                        'file_name': f.name,
                        'setting_size': filesizeformat(
                            settings.DASHBOARD_UPLOAD_FILE_MAX_SIZE),
                        'file_size': filesizeformat(f._size)
                        },
                    code='file_size'
                        )
                        )
        # check it is one of our allowed file types
        else:
            file_errors.append(ValidationError(
                _('%(file_name)s has not been uploaded: '\
                'File type is not supported'),
                params={'file_name': f.name},
                code='file_type'
                )
                )
        # next check the file hasn't been uploaded before
        # generate filehash
        file_hash = GenerateFileHash(f, self.user.username)
        f.seek(0)

        if Track.objects.filter(file_hash=file_hash).exists():
            file_errors.append(ValidationError(
                _('%(file_name)s has not been uploaded as an identical '\
                'file has already been uploaded previously'),
                params={'file_name': f.name},
                code='file_hash'))

        # next check the file is a valid gpx file
        try:
            parser.XMLParser(f.read().decode('ascii'))
            f.seek(0)
        except:
            file_errors.append(ValidationError(
                _('%(file_name)s is not a valid gpx file'),
                params={'file_name': f.name},
                code='invalid_gpx'))

        # finally raise errors if there are any
        if len(file_errors) > 0:
            self.fail( ValidationError(file_errors))
        else:
            return f
