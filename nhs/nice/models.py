from django.db import models

from prescriptions.models import Product

class Recommendation(models.Model):
    drug      = models.ForeignKey(Product)
    date      = models.DateField()
    guideline = models.CharField(max_length = 200)
    link      = models.URLField()
