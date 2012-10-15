"""
Urls for the APIs we propose to expose to the outside world
"""
from django.conf.urls.defaults import patterns, url

from nhs.api.views import Drug, DrugHabits, LocalDrug, PracticeHabits, Practices

urlpatterns = patterns(
    '',
    url(r'drug/$',                  Drug.as_view(),           name='drugapi'),
    url(r'drug/habits/$',           DrugHabits.as_view(),     name = "drughabitsapi"),
    url(r'drug/habits/location/$',  LocalDrug.as_view(),      name='localdrugapi'),
    url(r'practice/habits/$',       PracticeHabits.as_view(), name='practicehabitsapi'),
    url(r'practice/$',              Practices.as_view(),       name='practiceapi')
    )
