"""
Urls for the APIs we propose to expose to the outside world
"""
from django.conf.urls.defaults import patterns, url, include

from tastypie.api import Api

from practices.api import PracticeResource
from prescriptions.api import ProductResource, PrescriptionComparisonResource, PrescriptionResource, GroupResource
from ccgs.api import CCGResource

v1_api = Api(api_name='v1')
v1_api.register(PracticeResource())
v1_api.register(ProductResource())
v1_api.register(PrescriptionComparisonResource())
v1_api.register(PrescriptionResource())
v1_api.register(GroupResource())
v1_api.register(CCGResource())


urlpatterns = patterns(
    include(v1_api.urls), #both needed, not sure why.  Leaving for now. :/
    url('', include(v1_api.urls)),
    
    # Old, replaced with tastypie
    # '',
    # url(r'drug/$',                  Drug.as_view(),           name='drugapi'),
    # url(r'drug/habits/$',           DrugHabits.as_view(),     name = "drughabitsapi"),
    # url(r'drug/habits/location/$',  LocalDrug.as_view(),      name='localdrugapi'),
    # url(r'group/habits/$',          GroupHabits.as_view(),     name = "grouphabitsapi"),
    # url(r'practice/habits/$',       PracticeHabits.as_view(), name='practicehabitsapi'),
    # url(r'practice/$',              Practices.as_view(),       name='practiceapi'),
    # url(r'ccg/$',                  CCGs.as_view(),           name='ccgapi'),
    # url(r'ccg/habits/$',           CCGHabits.as_view(),     name = "ccghabitsapi"),
    )
