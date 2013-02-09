"""
Urls for the APIs we propose to expose to the outside world
"""
from django.conf.urls.defaults import patterns, url
from django.views.generic import TemplateView

from nhs.explore.views import Ratio, ExploreDrug

urlpatterns = patterns(
    '',
    url(r'/ratio/?$', Ratio.as_view(template_name='explore_compare.html'),
        name='explorecompare'),
    url(r'/drug/?$', ExploreDrug.as_view(template_name='explore_drug.html'),
        name='exploredrug'),
    url(r'/?$', TemplateView.as_view(template_name='explore.html'), name='explore'),
    )
