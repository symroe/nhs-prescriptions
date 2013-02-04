from django.conf import settings
from django.conf.urls.defaults import patterns, url, include
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

#from django.contrib.gis import admin
admin.autodiscover()

from nhs.nice.models import Recommendation

def getrecs():
    return Recommendation.objects.all()[0]

urlpatterns = patterns(
    '',
    url('^$', TemplateView.as_view(template_name='home.html'), name='home'),

    url(r'^explore', include('nhs.explore.urls')),

    url('^research/inhaler/?$', TemplateView.as_view(template_name='inhaler.html'), name='inhaler'),
    # API

    url(r'^api/', include('nhs.api.urls')),


    # Examples
    url(r'^examples/group/statins/$',
        TemplateView.as_view(template_name='examples/statins.html'), name='statgraph'),

#    url(r'^mapit/', include('mapit.urls')),


    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

)

urlpatterns += staticfiles_urlpatterns()
