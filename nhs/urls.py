from django.conf import settings
from django.conf.urls.defaults import patterns, url, include
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin

#from django.contrib.gis import admin
#admin.autodiscover()

from nhs.nice.models import Recommendation

def getrecs():
    return Recommendation.objects.all()[0]

urlpatterns = patterns(
    '',
    url('^$', TemplateView.as_view(template_name='home.html'), name='home'),

    # API
    url(r'^api/', include('nhs.api.urls')),

    
    # Examples
    url(r'^examples/group/statins/$', TemplateView.as_view(template_name='examples/statins.html'), name='statgraph'),
    url(r'^examples/patents/statins/$', TemplateView.as_view(template_name='examples/patins.html'), name='statgraph'),
    url(r'^examples/patents/practice/$', TemplateView.as_view(template_name='examples/patentpractice.html'), name='statgraph'),
    url(r'^examples/nice/$', TemplateView.as_view(template_name='examples/nice.html', get_context_data=lambda:{'rec':getrecs()}), name='statgraph'),
    url(r'^examples/lottery/',  'api.views.lottery'),
    url(r'^mapit/', include('mapit.urls')),


    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    #(r'^admin/', include(admin.site.urls)),

)

urlpatterns += patterns(
    '',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)
