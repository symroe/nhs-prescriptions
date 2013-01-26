# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.gis.db import models as geo_models
from nhs.ccgs.models import CCG

from mapit.models import Postcode

class Practice(geo_models.Model):
    practice = models.CharField(blank=True, max_length=100, primary_key=True)
    name = models.CharField(blank=True, max_length=255)
    location = geo_models.PointField(spatial_index=True, geography=False, null=True)
    postcode = models.CharField(blank=True, max_length=10)
    pc = models.ForeignKey(Postcode, null=True, blank=True)
    imd = models.FloatField(blank=True, null=True)
    address = models.TextField(blank=True)
    ccg = models.ForeignKey(CCG, null=True)
    objects = geo_models.GeoManager()

    def __unicode__(self):
        return "%s (%s)" % (self.pk, self.name)

