from tastypie.contrib.gis.resources import ModelResource as GeoModelResource

from models import CCG


class CCGResource(GeoModelResource):
    class Meta:
            model = CCG