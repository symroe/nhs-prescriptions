# -*- coding: utf-8 -*-

# the calculations in this file are based on the Javascript at: 
# http://www.movable-type.co.uk/scripts/latlong-gridref.html

# Useful links to understand this stuff (esp. adding support for the Irish Grid):
# http://en.wikipedia.org/wiki/British_national_grid_reference_system
# http://en.wikipedia.org/wiki/Irish_grid_reference_system#Summary_parameters_of_the_Irish_Grid_coordinate_system
# http://www.nisra.gov.uk/geography/default.asp6.htm
# http://www.nisra.gov.uk/geography/default.asp14.htm
# http://en.wikipedia.org/wiki/Transverse_Mercator
# http://en.wikipedia.org/wiki/Irish_Transverse_Mercator#Comparison_of_ITM.2C_Irish_Grid_and_UTM

import sys,math,re

# ellipse parameters
# See Constants for Reference Ellipsoids used for Datum Transformations:
# http://www.arsitech.com/mapping/geodetic_datum/

ellipse = {
    'WGS84': {
        'a': 6378137,
        'b': 6356752.3142,
        'f': 1/298.257223563
	},
    'Airy1830': {
        'a': 6377563.396,
        'b': 6356256.910,
        'f': 1/299.3249646
	},
    'AiryModified': {
        'a': 6377340.189,
        'b': 6356034.448,
        'f': 0.0033408506318589907
	}
    }

# helmert transform parameters
# see: http://en.wikipedia.org/wiki/Helmert_transformation
# Standard parameters: Note that the rotation angles given in the table
# are in seconds and must be converted to radians before use in the calculation.
# +---------+-----+----------+--------+-------+--------+---------+-----------+-----------+-----------+
# |Region   |Start|Target    |cx      |cy     |cz      |s        |rx         |ry         |rz         |
# |         |datum|datum     |(Metre) |(Metre)|(Metre) |(ppm)    |(Arcsecond)|(Arcsecond)|(Arcsecond)|
# +---------+-----+----------+--------+-------+--------+---------+-----------+-----------+-----------+
# |Slovenia |D48  |D96       |409.545 |72.164 |486.872 |17.919665|−3.085957  |−5.469110  |11.020289  |
# |ETRS89   |     |          |        |       |        |         |           |           |           |
# +---------+-----+----------+--------+-------+--------+---------+-----------+-----------+-----------+
# |England, |WGS84|OSGB36    |−446.448|125.157|−542.06 |20.4894  |−0.1502    |−0.247     |−0.8421    |
# |Scotland,|     |          |        |       |        |         |           |           |           |
# |Wales    |     |          |        |       |        |         |           |           |           |
# +---------+-----+----------+--------+-------+--------+---------+-----------+-----------+-----------+
# |Ireland  |WGS84|Ireland   |−482.53 |130.596|−564.557|−8.15    |1.042      |0.214      |0.631      |
# |         |     |1965      |        |       |        |         |           |           |           |
# +---------+-----+----------+--------+-------+--------+---------+-----------+-----------+-----------+
# |Germany  |WGS84|DHDN      |−591.28 |−81.35 |−396.39 |−9.82    |1.4770     |−0.0736    |−1.4580    |
# +---------+-----+----------+--------+-------+--------+---------+-----------+-----------+-----------+
# |Germany  |WGS84|Bessel    |−582    |−105   |−414    |−8.3     |−1.04      |−0.35      |3.08       |
# |         |     |1841      |        |       |        |         |           |           |           |
# +---------+-----+----------+--------+-------+--------+---------+-----------+-----------+-----------+
# |Germany  |WGS84|Krassovski|−24     |123    |94      |−1.1     |−0.02      |0.26       |0.13       |
# |         |     |1940      |        |       |        |         |           |           |           |
# +---------+-----+----------+--------+-------+--------+---------+-----------+-----------+-----------+
# |Austria  |WGS84|MGI       |−577.326|−90.129|−463.920|−2.423   |5.137      |1.474      |5.297      |
# |(BEV)    |     |          |        |       |        |         |           |           |           |
# +---------+-----+----------+--------+-------+--------+---------+-----------+-----------+-----------+
# |USA      |WGS84|Clarke    |8       |−160   |−176    |0        |0          |0          |0          |
# |         |     |1866      |        |       |        |         |           |           |           |
# +---------+-----+----------+--------+-------+--------+---------+-----------+-----------+-----------+
#
# These are standard parameter sets for the 7-parameter transformation (or data transformation) 
# between two ellipsoids. For a transformation in the opposite direction, 
# the signs of all the parameters must be changed.

helmert = {
    'WGS84toOSGB36': {
        'tx': -446.448,
        'ty': 125.157,
        'tz': -542.060,	# m
        'rx': -0.1502,
        'ry': -0.2470,
        'rz': -0.8421,	# sec
        's': 20.4894 # ppm
	},
    'OSGB36toWGS84': {
        'tx': 446.448,
        'ty': -125.157,
        'tz': 542.060,
        'rx': 0.1502,
        'ry': 0.2470,
        'rz': 0.8421,
        's': -20.4894
	}
    }

grid_system = {
    'british': {
        'ellipse': ellipse['Airy1830'],
        'scale_factor': 0.9996012717,
        'origin_lat': 49 * math.pi/180,
        'origin_lon': -2 * math.pi/180,
        'false_northing': -100000,
        'false_easting': 400000
        },
    'irish': {
        'ellipse': ellipse['AiryModified'],
        'scale_factor': 1.000035,
        'origin_lat': 53.5 * math.pi/180,
        'origin_lon': -8 * math.pi/180,
        'false_northing': 250000,
        'false_easting': 200000
        }
    }


# pad a number with sufficient leading zeros to make it w chars wide
def padLZ(value,width):
    num = str(value)
    length = len(num)
    i = 0
    while i<width-length:
        num = '0%s' % (num)
        i = i + 1
    return num


# convert degrees to radians
def toRad(deg):
    return (deg * math.pi) / 180


# convert radians to degrees (signed)
def toDeg(rad):
    return (rad * 180) / math.pi


# convert numeric degrees to deg/min/sec latitude
def toLat(value,dp=None):
    # knock off initial '0' for lat!
    lat = toDMS(value,dp)[1:]
    if value<0:
        lat = lat + 'S'
    else:
        lat = lat + 'N'
    return lat


# convert numeric degrees to deg/min/sec longitude
def toLon(value,dp=None):
    lon = toDMS(value, dp)
    if value > 0:
        lon = lon + 'E'
    else:
        lon = lon + 'W'
    return lon

# convert numeric degrees to deg/min/sec
def toDMS(value,dp=None):
    # if no decimal places argument, round to int seconds
    if dp == None:
        dp = 0

    d = math.fabs(value) # (unsigned result ready for appending compass direction)
    deg = math.floor(d)
    _min = math.floor((d-deg)*60)
    sec = round( ( (d-deg-_min/60)*3600) ,dp)
    # fix any nonsensical rounding-up
    if sec==60:
        sec = round(0, dp)
        _min = _min + 1

    if _min==60:
        _min = 0
        deg = deg + 1

    if deg==360:
        deg = 0

    deg = int(math.floor(deg))
    _min = int(math.floor(_min))
    sec = int(math.floor(sec))

    # add leading zeros if required
    if deg<100:
        deg = '0' + str(deg)
    if deg<10:
        deg = '0' + str(deg)
    if _min<10:
        _min = '0' + str(_min)
    if sec<10:
        sec = '0' + str(sec)

    #return '%s\u00B0%s\u2032%s\u2033' % (str(deg),str(_min),str(sec))
    return '%s°%s′%s″' % (str(deg),str(_min),str(sec))


def DMStoDeg(DMS): 
    degLL = re.sub(r'^-','',DMS) # strip off any sign or compass dir'n
    degLL = re.sub(r'[NSEW]','',degLL)

    dms = re.split(r'[^0-9.]+',degLL) # split out separate d/m/s

    working = []
    for item in dms: # remove empty elements
        if (item==''):
            pass
        else:
            working.append(item)
    dms = working

    if len(dms) == 3: # interpret 3-part result as d/m/s
        deg = float(dms[0])/1 + float(dms[1])/60 + float(dms[2])/3600

    elif len(dms) == 2: # interpret 2-part result as d/m
        deg = float(dms[0])/1 + float(dms[1])/60

    elif len(dms) == 1: # decimal or non-separated dddmmss
        if re.search(r'[NS]',DMS):
            degLL = '0' + degLL # normalise N/S to 3-digit degrees
        deg = float(dms[0][0:3])/1 + float(dms[0][3:5])/60 + float(dms[0][5:])/3600
    else:
        return False

    if re.search(r'^-',DMS) or re.search(r'[WS]',DMS):
        deg = -deg # take '-', west and south as -ve

    return deg


# construct a LatLon object: arguments in numeric degrees
# note all LatLong methods expect & return numeric degrees (for lat/long & for bearings)
class LatLon(object):

    def __init__(self,lat,lon,height=0):
        self.lat = lat
        self.lon = lon
        self.height = height

    def __del__(self):
        pass

    def __repr__(self):
        return "%s, %s" % (toLat(self.lat), toLon(self.lon))


# convert OS grid reference to geodesic co-ordinates
def OSGridToLatLong(gridRef):
    gr = gridrefLetToNum(gridRef)
    return OSNumericToLatLong(gr)


def OSNumericToLatLong(gridRef):
    return GridToLatLong(gridRef,grid_system['british'])


def IrishNumericToLatLong(gridRef):
    return GridToLatLong(gridRef,grid_system['irish'])


def GridToLatLong(gridRef,grid):
    E = int(gridRef[0])
    N = int(gridRef[1])

    # Airy 1830 major & minor semi-axes

    a = grid['ellipse']['a']
    b = grid['ellipse']['b']

    # NatGrid scale factor on central meridian
    F0 = grid['scale_factor']

    # NatGrid true origin
    lat0 = grid['origin_lat']
    lon0 = grid['origin_lon']

    # northing & easting of true origin, metres
    N0 = grid['false_northing']
    E0 = grid['false_easting']

    # eccentricity squared
    e2 = 1 - (b*b) / (a*a)

    n = (a-b) / (a+b)
    n2 = n * n
    n3 = n * n * n
    
    lat = lat0
    M = 0

    # until < 0.01mm
    while (N-N0-M) >= 0.00001:
        lat = (N-N0-M) / (a*F0) + lat
        Ma = (1 + n + (5/4)*n2 + (5/4)*n3) * (lat-lat0)
        Mb = (3*n + 3*n*n + (21/8)*n3) * math.sin(lat-lat0) * math.cos(lat+lat0)
        Mc = ((15/8)*n2 + (15/8)*n3) * math.sin(2*(lat-lat0)) * math.cos(2*(lat+lat0))
        Md = (35/24)*n3 * math.sin(3*(lat-lat0)) * math.cos(3*(lat+lat0))
        # meridional arc
        M = b * F0 * (Ma - Mb + Mc - Md)    

    cosLat = math.cos(lat)
    sinLat = math.sin(lat)

    # transverse radius of curvature
    nu = a*F0/math.sqrt(1-e2*sinLat*sinLat)
    # meridional radius of curvature
    rho = a*F0*(1-e2)/math.pow(1-e2*sinLat*sinLat, 1.5)
    eta2 = nu/rho-1

    tanLat = math.tan(lat)
    tan2lat = tanLat*tanLat
    tan4lat = tan2lat*tan2lat
    tan6lat = tan4lat*tan2lat

    secLat = 1/cosLat

    nu3 = nu*nu*nu
    nu5 = nu3*nu*nu
    nu7 = nu5*nu*nu

    VII = tanLat/(2*rho*nu)
    VIII = tanLat/(24*rho*nu3)*(5+3*tan2lat+eta2-9*tan2lat*eta2)
    IX = tanLat/(720*rho*nu5)*(61+90*tan2lat+45*tan4lat)
    X = secLat/nu
    XI = secLat/(6*nu3)*(nu/rho+2*tan2lat)
    XII = secLat/(120*nu5)*(5+28*tan2lat+24*tan4lat)
    XIIA = secLat/(5040*nu7)*(61+662*tan2lat+1320*tan4lat+720*tan6lat)
    
    dE = (E-E0)
    dE2 = dE*dE
    dE3 = dE2*dE
    dE4 = dE2*dE2
    dE5 = dE3*dE2
    dE6 = dE4*dE2
    dE7 = dE5*dE2

    lat = lat - VII*dE2 + VIII*dE4 - IX*dE6
    lon = lon0 + X*dE - XI*dE3 + XII*dE5 - XIIA*dE7
    
    return LatLon(toDeg(lat), toDeg(lon));


# convert standard grid reference ('SU387148') to fully numeric ref ([438700,114800])
# returned co-ordinates are in metres, centred on grid square for conversion to lat/long
#
# note that northern-most grid squares will give 7-digit northings
# no error-checking is done on gridref (bad input will give bad results or NaN)
def gridrefLetToNum(gridref):
    # get numeric values of letter references, mapping A->0, B->1, C->2, etc:
    l1 = ord(gridref[0].upper()) - ord('A')
    l2 = ord(gridref[1].upper()) - ord('A')

    # shuffle down letters after 'I' since 'I' is not used in grid:
    if l1 > 7:
	l1 = l1 - 1
    if l2 > 7:
	l2 = l2 - 1

    # convert grid letters into 100km-square indexes from false origin (grid square SV):
    e = str(((l1-2) % 5) * 5 + (l2 % 5))
    n = str( int(19 - math.floor(l1/5) *5) - int(math.floor(l2/5)) )

    # skip grid letters to get numeric part of ref, stripping any spaces:
    gridref = gridref[2:].replace(' ','')
    
    # append numeric part of references to grid index:
    e = e + gridref[:(len(gridref)/2)]
    n = n + gridref[(len(gridref)/2):]
    
    if len(gridref) == 6:
        e = e + '50'
        n = n + '50'
    elif len(gridref) == 8:
        e = e + '5'
        n = n + '5'
    else:
        # 10-digit refs are already 1m
        pass
    
    return [e, n]


# convert numeric grid reference (in metres) to standard-form grid ref
def gridrefNumToLet(e, n, digits):
    # get the 100km-grid indices
    e100k = int(math.floor(int(e)/100000))
    n100k = int(math.floor(int(n)/100000))

    if (e100k<0 or e100k>6 or n100k<0 or n100k>12):
        return ''

    # translate those into numeric equivalents of the grid letters
    l1 = (19-n100k) - (19-n100k) % 5 + math.floor((e100k+10)/5)
    l2 = (19-n100k) * 5 % 25 + e100k % 5;

    # compensate for skipped 'I' and build grid letter-pairs
    if l1 > 7:
        l1 = l1 + 1
    if l2 > 7:
        l2 = l2 + 1

    letPair = "%s%s" % (chr( 65 + int(l1) ),chr( 65 + int(l2) ))

    # strip 100km-grid indices from easting & northing, and reduce precision
    e = int(math.floor( (int(e) % 100000) / math.pow(10,5 - digits / 2)))
    n = int(math.floor( (int(n) % 100000) / math.pow(10,5 - digits / 2)))
    # note use of floor, as ref is bottom-left of relevant square!

    gridRef = '%s %s %s' % (letPair, padLZ(e,digits/2), padLZ(n,digits/2))

    return gridRef




def convertOSGB36toWGS84(p1):
    p2 = convert(p1, ellipse['Airy1830'], helmert['OSGB36toWGS84'], ellipse['WGS84'])
    return p2


def convertWGS84toOSGB36(p1):
    p2 = convert(p1, ellipse['WGS84'], helmert['WGS84toOSGB36'], ellipse['Airy1830'])
    return p2


def convert(p, e1, t, e2):
    # -- convert polar to cartesian coordinates (using ellipse 1)
    p1 = LatLon(p.lat, p.lon, p.height); # to avoid modifying passed param
    p1.lat = toRad(p.lat)
    p1.lon = toRad(p.lon)

    a = e1['a']
    b = e1['b']

    sinPhi = math.sin(p1.lat)
    cosPhi = math.cos(p1.lat)
    sinLambda = math.sin(p1.lon)
    cosLambda = math.cos(p1.lon)
    H = p1.height

    eSq = (a*a - b*b) / (a*a)
    nu = a / math.sqrt(1 - eSq * sinPhi * sinPhi)

    x1 = (nu+H) * cosPhi * cosLambda
    y1 = (nu+H) * cosPhi * sinLambda
    z1 = ( (1-eSq) * nu + H) * sinPhi
    
    # -- apply helmert transform using appropriate params

    tx = t['tx']
    ty = t['ty']
    tz = t['tz']
    rx = t['rx']/3600 * math.pi/180 # normalise seconds to radians
    ry = t['ry']/3600 * math.pi/180
    rz = t['rz']/3600 * math.pi/180
    s1 = t['s']/1e6 + 1; # normalise ppm to (s+1)

    # apply transform
    x2 = tx + x1 * s1 - y1 * rz + z1 * ry
    y2 = ty + x1 * rz + y1 * s1 - z1 * rx
    z2 = tz - x1 * ry + y1 * rx + z1 * s1

    # -- convert cartesian to polar coordinates (using ellipse 2)

    a = e2['a']
    b = e2['b']
    precision = 4 / a # results accurate to around 4 metres

    eSq = (a*a - b*b) / (a*a)
    p = math.sqrt(x2*x2 + y2*y2)
    phi = math.atan2(z2, p*(1-eSq))
    phiP = 2*math.pi
    while (math.fabs(phi-phiP) > precision):
        nu = a / math.sqrt(1 - eSq*math.sin(phi)*math.sin(phi))
        phiP = phi
        phi = math.atan2(z2 + eSq*nu*math.sin(phi), p)

    lmbda = math.atan2(y2, x2)
    H = p/math.cos(phi) - nu;
    
    return LatLon(toDeg(phi), toDeg(lmbda), H)


# function LatLon(lat, lon, rad) {
#   if (typeof rad == 'undefined') rad = 6371;  // earth's mean radius in km
#   this._lat = lat;
#   this._lon = lon;
#   this._radius = rad;
# }


 # * Returns the distance in km 
 # * (using Haversine formula)
 # *
 # * from: Haversine formula - R. W. Sinnott, "Virtues of the Haversine",
 # *       Sky and Telescope, vol 68, no 2, 1984
 # *
 # * @param   {LatLon} start: Start point
 # * @param   {LatLon} end: Start point
 # * @param   {Number} precision: required result precision (in m)
 # * @returns {Number} Distance
def distanceTo(start,end, precision=4):
    R = 6371 # earth's mean radius in km
    lat1 = toRad(start.lat)
    lon1 = toRad(start.lon)
    lat2 = toRad(end.lat)
    lon2 = toRad(end.lon)
    dLat = lat2 - lat1
    dLon = lon2 - lon1

    a = math.sin(dLat/2) * math.sin(dLat/2) + \
        math.cos(lat1) * math.cos(lat2) * \
        math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    # return d.toPrecisionFixed(precision);
    return round(d,precision)


 # * Returns the destination point from the start point having travelled the given distance (in km) on the 
 # * given initial bearing (bearing may vary before destination is reached)
 # *
 # *   see http://williams.best.vwh.net/avform.htm#LL
 # *
 # * @param   {LatLon} start: Start point
 # * @param   {Number} brng: Initial bearing in degrees
 # * @param   {Number} dist: Distance in km
 # * @returns {LatLon} Destination point
def destinationPoint(start, brng, dist):
    R = 6371 # earth's mean radius in km

    dist = float(dist)/R # convert dist to angular distance in radians

    brng = toRad(brng)
    lat1 = toRad(start.lat)
    lon1 = toRad(start.lon)

    lat2 = math.asin( math.sin(lat1) * math.cos(dist) + math.cos(lat1) * math.sin(dist) * math.cos(brng) )
    lon2 = lon1 + math.atan2(math.sin(brng) * math.sin(dist) * math.cos(lat1), math.cos(dist) - math.sin(lat1) * math.sin(lat2))
    lon2 = (lon2+3 * math.pi) % (2*math.pi) - math.pi # normalise to -180...+180

    # if (isNaN(lat2) || isNaN(lon2)) return null;

    return LatLon(toDeg(lat2), toDeg(lon2))

