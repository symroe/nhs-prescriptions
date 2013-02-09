import sys
import csv
from optparse import make_option

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
    option_list = BaseCommand.option_list + (
        make_option('--filename', '-f', dest='filename',),
        )

    def process_line(self, line):
#        import pdb; pdb.set_trace()
        print line
        pk = line[1]
        try:
            P = Practice.objects.get(name=pk)
        except Practice.DoesNotExist:
            P = Practice(name=pk, practice=pk)
        print 'p is ', P
        P.name = line[1].title()
        P.postcode = line[-2]
        P.address = "\n".join([x.title() for x in line[2:]])

        print P.name, P.postcode, P.address
        P.save()
        print "Saved %s" % P

    def handle(self, **options):
        self.filename = options['filename']
        seen = set()

        infile = csv.reader(ReadlineIterator(open(self.filename, 'r')))
        for line in infile:
            line = [x.strip() for x in line]

            if not line[1] in seen:
                seen.add(line[1])
                self.process_line(line)
