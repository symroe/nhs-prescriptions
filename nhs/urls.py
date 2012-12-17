from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin

#from django.contrib.gis import admin
#admin.autodiscover()

urlpatterns = patterns(
    '',
    url('^$', TemplateView.as_view(template_name='home.html'), name='home'),
    # API
    url(r'^api/', include('nhs.api.urls')),
    # Examples
    url(r'^examples/group/statins/$', TemplateView.as_view(template_name='examples/statins.html'), name='statgraph'),

    url(r'^mapit/', include('mapit.urls')),


    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    #(r'^admin/', include(admin.site.urls)),

)

urlpatterns += patterns(
    '',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)
