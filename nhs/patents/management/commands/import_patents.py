"""
Import Patents
"""
import datetime
from optparse import make_option

from django.core.management.base import BaseCommand
import ffs

from nhs.patents.models import Patent
from nhs.prescriptions.models import Product

class Command(BaseCommand):
    """
    Our command!

    Import the patent data
    """
    option_list = BaseCommand.option_list + (
        make_option('--filename', '-f', dest='filename',),
        )

    def handle(self, **options):
        "IDjangoManagementCommand Entrypoint!"
        assert options['filename']
        csvfile = ffs.Path(options['filename'])
        with csvfile.csv(header=True) as csv:
            for expiry in csv:
                drugs = Product.objects.filter(name=expiry.name)

                for drug in drugs:
                        expiry_date = datetime.datetime.strptime(expiry.expiry, '%d/%m/%Y')
                        patent = Patent.objects.get_or_create(drug=drug, expiry_date = expiry_date)[0]
                        patent.save()

