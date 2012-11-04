"""
Import Nice recommendations
"""
import datetime
from optparse import make_option

from django.core.management.base import BaseCommand
import ffs

from nhs.patents.models import Patent
from nhs.prescriptions.models import Product
from nhs.nice.models import Recommendation

class Command(BaseCommand):
    """
    Our command!

    Import the nice guidelines
    """
    option_list = BaseCommand.option_list + (
        make_option('--filename', '-f', dest='filename',),
        )

    def handle(self, **options):
        "IDjangoManagementCommand Entrypoint!"
        assert options['filename']
        csvfile = ffs.Path(options['filename'])

        names = [d.name for d in Product.objects.all()]

        with csvfile.csv(header=True) as csv:
            for recc in csv:
                print recc
                drugs = [n for n in names if n in recc.title]
                if len(drugs) > 0:
                    print recc
                    print drugs
                    for d in drugs:
                        date = datetime.datetime.strptime(recc.date, '%Y-%m')
                        modeldrug = Product.objects.get(name=d)
                        recc = Recommendation.objects.get_or_create(drug=modeldrug, date=date,
                                                                    guideline=recc.title, link = recc.link)[0]
                        recc.save()


