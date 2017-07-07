from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.reverse import reverse


class ModelTestCase(TestCase):
    # This class defines the test suite for the openrun model.

    def setUp(self):
        # Define the test client and other test variables.
        self.user = User(username='temporary1', password='temporary1')

    def test_model_can_create_user(self):
        old_count = User.objects.count()
        self.user.save()
        new_count = User.objects.count()
        self.assertNotEqual(old_count, new_count)


class viewTestCase(TestCase):
    # Test suite for the api views.

    def setUp(self):
        # Define the test client and other test variables.

        self.staff_user = User.objects.create(
            username='staff',
            is_staff=True,)
        self.normal_user = User.objects.create(
            username='user',
            is_staff=False,)
        self.client = APIClient()



class uploadTestCase(TestCase):
    # Test suite for the file upload section.

    def setUp(self):
        valid_gpx = '<?xml version="1.0" encoding="UTF-8"?>\
                <gpx version="1.1">\
                <trk>\
                <name><![CDATA[Running 4/15/10 6:04 pm]]></name>\
                <time>2010-04-15T18:04:28Z</time>\
                <trkseg>\
                <trkpt lat="51.443217000" lon="-2.610013000">\
                <ele>69.7</ele>\
                <time>2010-04-15T18:04:28Z</time>\
                </trkpt>\
                <trkpt lat="51.443946000" lon="-2.610618000">\
                <ele>72.9</ele>\
                <time>2010-04-15T18:05:08Z</time>\
                </trkpt>\
                </trkseg>\
                <trkseg>\
                <trkpt lat="51.443638000" lon="-2.614061000">\
                <ele>79.6</ele>\
                <time>2010-04-15T18:07:20Z</time>\
                </trkpt>\
                <trkpt lat="51.443255000" lon="-2.615090000">\
                <ele>81.0</ele>\
                <time>2010-04-15T18:07:33Z</time>\
                </trkpt>\
                </trkseg>\
                </trk>\
                </gpx>'.encode('utf-8')

        invalid_gpx = '<?xml version="1.0" encoding="UTF-8"?>\
                <gpx version="1.1">\
                <trk>\
                <name><![CDATA[Running 4/15/10 6:04 pm]]></name>\
                <time>2010-04-15T18:04:28Z</time>\
                <trkseg>\
                <trkpt lat="51.443217000" lon="-2.610013000">\
                <ele>69.7</ele>\
                <trkpt lat="51.443255000" lon="-2.615090000">\
                <ele>81.0</ele>\
                <time>2010-04-15T18:07:33Z</time>\
                </trkpt>\
                </trk>\
                </gpx>'.encode('utf-8')

        self.staff_user = User.objects.create(
            username='staff',
            is_staff=True,)
        self.normal_user = User.objects.create(
            username='user',
            is_staff=False,)
        self.client = APIClient()

        self.file_dict_1 = {'file': SimpleUploadedFile(
            'test.gpx', valid_gpx, 'text/xml')}
        self.file_dict_2 = {'file': SimpleUploadedFile(
            'test.gpx', valid_gpx, 'text/xml')}
        self.file_dict_3 = {'file': SimpleUploadedFile(
            'test.gpx', invalid_gpx, 'text/xml')}
        self.file_dict_4 = {'file': SimpleUploadedFile(
            'test.gpx', invalid_gpx, 'virus/trojan')}
        self.client.force_authenticate(user=self.staff_user)

    def test_api_can_upload_file(self):

        resp = self.client.post(reverse('upload'), self.file_dict_1)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_api_cant_upload_file_twice(self):
        resp = self.client.post(reverse('upload'), self.file_dict_1)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        resp = self.client.post(reverse('upload'), self.file_dict_2)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_cant_upload_invalid_gpx_file(self):
        resp = self.client.post(reverse('upload'), self.file_dict_3)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_cant_upload_invalid_file_type(self):
        resp = self.client.post(reverse('upload'), self.file_dict_4)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
