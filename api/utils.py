from hashlib import md5
from pytz import utc
from fiona import open

from django.contrib.gis.geos import LineString, MultiLineString

from .models import Track

from gpxpy import parse


def SaveGPXtoModel(f, owner):

    # parse gpx file
    gpx = parse(f.read().decode('utf-8'))
    f.seek(0)

    layer = open(f.temporary_file_path(), layer='tracks')

    # get moving data
    moving_data = gpx.get_moving_data()

    # generate hash
    file_hash = GenerateFileHash(f, owner.username)

    # import track data and create start, stop, pause and resume points
    if gpx.tracks:
        for track in gpx.tracks:
            new_track = Track()
            new_track.file_hash = file_hash
            new_track.owner = owner
            new_track.start = utc.localize(track.get_time_bounds().start_time)
            new_track.finish = utc.localize(track.get_time_bounds().end_time)
            new_track.average_speed = (moving_data[2] / 1000) \
                / (moving_data[0] / 3600)
            new_track.duration = moving_data[0] / 3600
            new_track.distance = moving_data[2] / 1000
            multi_line_string = []
            for line_string in layer[0]['geometry']['coordinates']:
                multi_line_string.append(LineString(line_string))
            new_track.track = MultiLineString(multi_line_string)

            new_track.save()

            return new_track


def GenerateFileHash(f, username):
    # generate MD5
    md5hash = md5()
    for chunk in f.chunks():
        md5hash.update(chunk)
    md5hash.update(username.encode('utf-8'))
    return md5hash.hexdigest()
