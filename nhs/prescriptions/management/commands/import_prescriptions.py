import sys
import csv
from optparse import make_option

from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from django.db import connection, backend, models

from prescriptions.models import Product, Prescription
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
        make_option('--date', '-d', dest='date',),
        )

    def __init__(self):
        self.cursor = connection.cursor()
        self.columns = ",".join([
            'product_id',
            'practice_id',
            'quantity',
            'nic',
            'actual_cost',
            'period',
        ])
        self.product_cols = ",".join([
                'bnf_code',
                'name'
            ])

    def copy(self):
        print self.filename
        sql = """
            DELETE FROM prescriptions_prescription WHERE period = '%(period)s';
        """ % {
            'period' : self.period,
        }
        self.cursor.execute(sql)

        sql = """
            COPY prescriptions_product (%(columns)s)
            FROM '%(filename)s'
            DELIMITERS ','
            CSV;
            COMMIT;
        """ % {
            'filename': self.product_filename,
            'columns': self.product_cols
            }
        self.cursor.execute(sql)

        sql = """
            COPY prescriptions_prescription (%(columns)s)
            FROM '%(filename)s'
            DELIMITERS ','
            CSV;
            COMMIT;
        """ % {
            'filename' : self.filename,
            'columns' : self.columns,
        }
        print sql
        self.cursor.execute(sql)

    def clean_data(self):

        known_bnfs = [p.pk for p in Product.objects.all()]

        infile = csv.reader(open(self.filename))
        infile.next()
        outfile = csv.writer(open('/tmp/data.csv', 'w'))
        product_file = csv.writer(open('/tmp/product.csv', 'w'))

        self.filename = "/tmp/data.csv"
        self.product_filename = "/tmp/product.csv"

        for line in infile:
            line = [x.strip() for x in line]

            outfile.writerow([
                line[3],
                line[2],
                line[5],
                line[6],
                line[7],
                line[8],
            ])

            if line[3] not in known_bnfs:
                known_bnfs.append(line[3])
                product_file.writerow([
                        line[3],
                        line[4]
                        ])

    def handle(self, *args, **options):
        assert options['filename']
        assert options['date']
        self.filename = options['filename']
        self.period = options['date']
        self.clean_data()
        self.copy()

