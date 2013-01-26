from tastypie.contrib.gis.resources import ModelResource as GeoModelResource

from models import Practice


class PracticeResource(GeoModelResource):
    class Meta:
            model = Practice
            resource_name = 'practice'