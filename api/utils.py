from hashlib import md5
from pytz import utc
from fiona import open

from django.contrib.gis.geos import Point, LineString, MultiLineString

from .models import Track, TrackPoint

from gpxpy import parse


def SaveGPXtoModel(f, owner):

    # parse gpx file
    gpx = parse(f.read().decode('utf-8'))
    f.seek(0)

    # get moving data
    moving_data = gpx.get_moving_data()

    # generate hash
    file_hash = GenerateFileHash(f, owner.username)

    # import track data
    if gpx.tracks:
        for track in gpx.tracks:

            tracks = open(f.temporary_file_path(), layer='tracks')

            # generate multi line string
            multi_line_string = []
            for line_string in tracks[0]['geometry']['coordinates']:
                multi_line_string.append(LineString(line_string))

            # create new track
            new_track = Track(
                file_hash=file_hash,
                owner=owner,
                start=utc.localize(track.get_time_bounds().start_time),
                finish=utc.localize(track.get_time_bounds().end_time),
                average_speed=(
                    (moving_data[2] / 1000)
                    /
                    (moving_data[0] / 3600)
                    ),
                duration=moving_data[0] / 3600,
                distance=moving_data[2] / 1000,
                track=MultiLineString(multi_line_string)
                )
            new_track.save()

            for segment_id, segment in enumerate(track.segments):
                for point_id, point in enumerate(segment.points):

                    speed = segment.get_speed(point_id)
                    if point_id == 0:
                        speed = 0
                        if segment_id == 0:
                            point_type = 'S'
                        else:
                            point_type = 'R'
                    elif point_id == len(segment.points)-1:
                        if segment_id == len(track.segments)-1:
                            point_type = 'F'
                        else:
                            point_type = 'P'
                    else:
                        point_type='A'

                    new_point = TrackPoint(
                        track=new_track,
                        point_type=point_type,
                        point=Point(
                            point.longitude,
                            point.latitude
                            ),
                        time=point.time,
                        elevation=point.elevation,
                        segment_id=segment_id,
                        speed=speed,
                        )
                    new_point.save()

            return new_track


def GenerateFileHash(f, username):
    # generate MD5
    md5hash = md5()
    for chunk in f.chunks():
        md5hash.update(chunk)
    md5hash.update(username.encode('utf-8'))
    return md5hash.hexdigest()
