"""
Urls for the APIs we propose to expose to the outside world
"""
from django.conf.urls.defaults import patterns, url, include

from tastypie.api import Api

from practices.api import PracticeResource
from prescriptions.api import (ProductResource, PrescriptionComparisonResource,
                               PrescriptionResource, GroupResource,
                               PrescriptionAggregatesResource)
from ccgs.api import CCGResource, CCGMetadataResource

v1_api = Api(api_name='v1')
v1_api.register(PracticeResource())
v1_api.register(ProductResource())
v1_api.register(PrescriptionComparisonResource())
v1_api.register(PrescriptionResource())
v1_api.register(PrescriptionAggregatesResource())
v1_api.register(GroupResource())
v1_api.register(CCGResource())
v1_api.register(CCGMetadataResource())

urlpatterns = patterns(
    '',
    url(r'doc/', include('tastypie_swagger.urls', namespace='tastypie_swagger')),
    # include(v1_api.urls), #both needed, not sure why.  Leaving for now. :/
    url('', include(v1_api.urls)),
    )
