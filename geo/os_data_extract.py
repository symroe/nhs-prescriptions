"""os_extract_data.py
Extract postcodes and map reference co-ordinates from the Ordnance Survey Code Point Open data,
and create a database of locations which allows us to map postcodes to lat long values.
This requires the map references to be converted to projection co-ordinates.

Because the Ordnance survey uses a different projection mechanism to most GPS, there is an 
additional conversion to re-map the returned latlong co-ordinates (e.g. OSGB36 -> WGS84).
"""

import os

from sqlite3 import *
import geo_utils as geo

# path to Ordnance Survey csv data
# (download http://data.gov.uk/dataset/os-code-point-open)
data_dir = 'Code-Point Open/Data'

database_file = 'locations.db'

# re-create the database if it already exists.
if os.path.exists(database_file):
    os.remove(database_file)

# locations = {}
conn = connect(database_file)
curs = conn.cursor()

def process_file(path):
    print 'processing: %s' % (path)
    f = open(path,'r')
    while True:
        data = f.readline()
        if not data:
            break
        else:
            e = data.split(',')[10]
            n = data.split(',')[11]

            OSGB36 = geo.OSNumericToLatLong([e,n])
            WGS84 = geo.convertOSGB36toWGS84(OSGB36)

            curs.execute( \
                "insert into postcodes values (NULL,?,?,?,?,?)", \
                    ( data.split(',')[0][1:-1], \
                          data.split(',')[10], \
                          data.split(',')[11], \
                          WGS84.lat, \
                          WGS84.lon ))
    f.close()
    conn.commit()

# create postcodes table
curs.execute('create table postcodes (id integer primary key, postcode text unique, easting text, northing text, lat real, long real)')

for file_name in os.listdir(data_dir):
    full_path = os.path.join(data_dir,file_name)
    if os.path.isfile(full_path) and full_path.endswith('.csv'):
        process_file(full_path)
