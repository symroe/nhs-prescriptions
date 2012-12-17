
from django.contrib.gis.geos import MultiPolygon, Polygon

def get_geometry(polygons):
    d = {'type': 'FeatureCollection'}
    d['features']= [{'type': 'Feature', 'coordinates': poly.coords} for poly in polygons]
    return d