# -*- coding: utf-8 -*-
from django.db import models

from practices.models import Practice

# Create your models here.
class Product(models.Model):
    bnf_code = models.CharField(blank=True, max_length=100, primary_key=True)
    name = models.CharField(blank=True, max_length=255, db_index=True)

class Prescription(models.Model):
    product = models.ForeignKey(Product)
    practice = models.ForeignKey(Practice)
    quantity = models.IntegerField(blank=True, null=True)
    nic = models.FloatField()
    actual_cost = models.FloatField()
    period = models.IntegerField(blank=True, null=True, db_index=True)