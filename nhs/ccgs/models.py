# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.gis.db import models as geo_models
from django_extensions.db.fields import AutoSlugField

class CCG(geo_models.Model):
    title = models.CharField(max_length=100)
    name = AutoSlugField(populate_from='title')
    code = models.CharField(max_length=5)
    region = models.CharField(max_length=32)
    population = models.IntegerField()
    lsoa_count = models.IntegerField()
    poly = geo_models.MultiPolygonField()

    objects = geo_models.GeoManager()

    def __unicode__(self):
        return "%s (%s)" % (self.pk, self.name)
