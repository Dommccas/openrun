from rest_framework.renderers import BaseRenderer
from django.contrib.gis.geos import GEOSGeometry

from django.template import loader


class SVGRenderer(BaseRenderer):

    media_type = 'image/svg+xml'
    format = 'svg'
    template_name = 'api/track.svg'

    def render(self, data, accepted_media_type=None, renderer_context=None):

        total_extent = []
        svgpaths = []

        try:
            features = data['results']['features']
        except:
            features = [data]

        for feature in features:

            try:
                height = int(
                    renderer_context['request'].query_params['height']
                    )
                width = int(
                    renderer_context['request'].query_params['width']
                    )
            except:
                height = 1000
                width = 1000

            geometry = GEOSGeometry(str(feature['geometry']))
            total_extent.append(geometry.extent)

            for line in geometry:
                tmpPath = 'M ' + str(line[0][0]) + ' ' + str(line[0][1])
                for point in line[1:]:
                    tmpPath += ' L ' + str(point[0]) + ' ' + str(point[1])
                svgpaths.append(tmpPath)

        unzipped = list(zip(*total_extent))

        translate = 'translate(%s %s)' % (
            -1 * min(unzipped[0]),
            -1 * min(unzipped[1])
            )

        max_range_x = max(unzipped[2]) - min(unzipped[0])
        max_range_y = max(unzipped[3]) - min(unzipped[1])

        scale = 'scale(%s)' % (
            min(height, width)
            /
            max(max_range_x, max_range_y)
            )

        stroke_width =  max(max_range_x, max_range_y) / min(height, width)

        template = loader.get_template(self.template_name)

        return template.render({
            'paths': svgpaths,
            'translate': translate,
            'scale': scale,
            'height': height,
            'width': width,
            'stroke_width': stroke_width,
            })
