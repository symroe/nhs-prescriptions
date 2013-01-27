"""
Command to link the existing practice data to Mapit Postcodes
"""
from django.core.management.base import BaseCommand

from mapit.models import Postcode

from practices.models import Practice



class Command(BaseCommand):
    def handle(self,**options):
        for practice in Practice.objects.all():
            pc = Postcode.objects.filter(postcode=practice.postcode)
            if len(pc) == 0:
                continue
                print practice.postcode
            else:
                pc = pc[0]
            practice.pc = pc
            practice.save()
