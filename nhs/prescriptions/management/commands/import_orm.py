"""
This will be SLOW for everything, but is the simplest thing that could
possibly work for the STATIN subset.
"""
from optparse import make_option

from nhs.prescriptions.model import

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--filename', '-f', dest='filename',),
        make_option('--date', '-d', dest='date',),
        )

    def handle(self, **options):
        assert options['filename']
        assert options['date']
        self.filename = options['filename']
        self.period = options['date']



