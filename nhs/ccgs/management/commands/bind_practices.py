from django.core.management.base import BaseCommand

from nhs.ccgs.models import CCG
from nhs.practices.models import Practice

class Command(BaseCommand):

    def handle(self, **options):
        for practice in Practice.objects.all():
            if not practice.location:
                continue

            ccgs = CCG.objects.filter(poly__contains=practice.location)
            if ccgs:
                practice.ccg = ccgs[0]
                practice.save()