from tastypie.contrib.gis.resources import ModelResource as GeoModelResource

from models import CCG


class CCGResource(GeoModelResource):
    class Meta:
        model = CCG
        queryset = CCG.objects.all()
        allowed_methods = ['get']

class CCGMetadataResource(GeoModelResource):
    """
    Provide an alternative API to retrieve just the metadata without the
    Geoms.
    """
    class Meta:
        model = CCG
        queryset = CCG.objects.all()
        allowed_methods = ['get']
        excludes = ['poly']

    def dehydrate(self, bundle):
        """
        Add the number of practices
        """
        bundle.data['no_of_practices'] = bundle.obj.practice_set.count()
        return bundle
