from tastypie import fields
from tastypie.contrib.gis.resources import ModelResource as GeoModelResource

from models import Practice
from mapit.models import Postcode

class MapitPostCodeResource(GeoModelResource):
    class Meta:
        queryset = Postcode.objects.all()

class PracticeResource(GeoModelResource):
    pc = fields.ToOneField(MapitPostCodeResource, 'pc', null=True)
    
    class Meta:
            model = Practice
            queryset = Practice.objects.all()


