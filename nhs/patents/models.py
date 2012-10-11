from django.db import models

from nhs.prescriptions.models import Product

class Patent(models.Model):
    drug        = models.ForeignKey(Product)
    expiry_date = models.DateField()
    start_date  = models.DateField(null=True, blank=True)
                        # Stupid. But you know, they're called patent numbers.
                        # Except they have letters in them.
    number      = models.CharField(max_length=200, null=True, blank=True)
