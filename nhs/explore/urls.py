"""
Urls for the APIs we propose to expose to the outside world
"""
from django.conf.urls.defaults import patterns, url

from nhs.explore.views import Ratio

urlpatterns = patterns(
    '',
    url(r'ratio/?$', Ratio.as_view(template_name='explore.html'), name='explore'),
    )
