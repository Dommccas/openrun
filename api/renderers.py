from rest_framework.renderers import BaseRenderer
from django.contrib.gis.geos import GEOSGeometry

from django.template import loader


class TemplateRenderer(BaseRenderer):

    template_name = None

    def render(self, data, accepted_media_type=None, renderer_context=None):

        svgpaths = []
        try:
            features = data['results']['features']
        except:
            features = [data]

        for feature in features:

            Geometry = GEOSGeometry(str(feature['geometry']))
            for line in Geometry:
                tmpPath = 'M ' + str(line[0][0]) \
                        + ' ' + str(line[0][1]) + ' L '
                for point in line[1:]:
                    tmpPath += str(point[0]) + ' ' + str(point[1]) + ' '
                svgpaths.append(tmpPath)

        template = loader.get_template(self.template_name)

        return template.render({'paths': svgpaths})


class SVGRenderer(TemplateRenderer):

    media_type = 'image/svg+xml'
    format = 'svg'
    template_name = 'api/features'
