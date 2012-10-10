import sys
import csv

from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point

from practices.models import Practice

class ReadlineIterator:
    """
    An iterator that calls readline() to get its next value.
    """
    def __init__(self, f): self.f = f
    def __iter__(self): return self
    def next(self):
        line = self.f.readline()
        if line: return line
        else: raise StopIteration

class Command(BaseCommand):
    
    def handle(self, **options):
        infile = csv.reader(ReadlineIterator(sys.stdin))
        for line in infile:
            line = [x.strip() for x in line]
            try:
                P = Practice.objects.get(pk=line[1])
            except Practice.DoesNotExist:
                P = Practice(pk=line.pop(1))
            P.name = line.pop(1).title()
            P.postcode = line.pop()
            P.address = "\n".join([x.title() for x in line[1:]])
            print P
            P.save()
            # sys.exit()