import sys
import csv
import optparse
from xml.dom.minidom import parseString
from django.contrib.gis.geos import MultiPolygon, Polygon

from django.core.management.base import BaseCommand

from ccgs.models import CCG

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
            optparse.make_option('-f', '--file',
                dest='filename',
                metavar="FILE",
                help='Specifies the input file'),
            )

    def handle(self, **options):
        if not options['filename']:
            print 'You need to specify the filename containing the CSV/KML data'
            sys.exit(1)

        # Naughty csv has some fields larger than 128Kb so we'll just make the
        # limit larger
        csv.field_size_limit(1310720)

        with open(options['filename'], 'rU') as f:
            reader = csv.reader(f)
            reader.next()  # skip header
            for row in reader:
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

            results.append(Polygon(polygons))

        return MultiPolygon(results)
