# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.gis.db import models as geo_models

class Practice(geo_models.Model):
    practice = models.CharField(blank=True, max_length=100, primary_key=True)
    name = models.CharField(blank=True, max_length=255)
    location = geo_models.PointField(spatial_index=True, geography=True, null=True)
    postcode = models.CharField(blank=True, max_length=10)
    address = models.TextField(blank=True)

    def __unicode__(self):
        return "%s (%s)" % (self.pk, self.name)

