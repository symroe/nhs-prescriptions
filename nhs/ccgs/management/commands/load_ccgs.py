import sys
import csv
import optparse
from xml.dom.minidom import parseString
from django.contrib.gis.geos import MultiPolygon, Polygon

from django.core.management.base import BaseCommand

from ccgs.models import CCG


class ReadlineIterator:
    """An iterator that calls readline() to get its next value."""
    def __init__(self, f): self.f = f
    def __iter__(self): return self
    def next(self):
        line = self.f.readline()
        if line: return line
        else: raise StopIteration


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
            optparse.make_option('-f', '--file',
                dest='filename',
                metavar="FILE",
                help='Specifies the input file'),
            )

    def process_row(self, row):
        if CCG.objects.filter(name=row[3]).count():
            ccg = CCG.objects.get(name=row[3])
            print 'Updating CCG for %s' % row[3]
        else:
            ccg = CCG()
            print 'Creating new CCG for %s' % row[3]
        ccg.title = row[3]
        ccg.code = row[2]
        ccg.population = int(row[5])
        ccg.lsoa_count = int(row[6])
        ccg.region = row[7]
        ccg.poly = self.get_geometry(row[8])
        ccg.save()

    def handle(self, **options):
        # Naughty csv has some fields larger than 128Kb so we'll just make the
        # limit larger
        csv.field_size_limit(1310720)
                
        reader = csv.reader(ReadlineIterator(sys.stdin))
        reader.next()  # skip header
        for row in reader:
            self.process_row(row)


    def get_geometry(self, data):
        """ Gets the geometry out of the provided KML as a MultiPolygon """
        dom = parseString(data)
        results = []

        coordinates = dom.getElementsByTagName('coordinates')
        for coord in coordinates:
            polygons = []

            for p in coord.firstChild.nodeValue.split(' '):
                x,y,_ = p.split(',')
                polygons.append( (float(x), float(y),) )

            try:
                polygons.append(polygons[0])
                P = Polygon(polygons)
                results.append(P)
            except:
                pass
        
        return MultiPolygon(results)
