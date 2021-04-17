from django.contrib.gis.geoip2 import GeoIP2


def get_ip_address(request):
    x_forward_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forward_for:
        ip = x_forward_for.split('.')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_geo(ip):
    g = GeoIP2()
    country = g.country(ip)
    city = g.city(ip)
    lat, lon = g.lat_lon(ip)
    return country, city, lat, lon

def get_center_cordinates(latA,longA,latB=None,longB=None):
    cord = (latA,longA)
    if latB:
        cord =[(latA+latB)/2,(longA+longB)/2]

    return cord

def get_zoom(distance):
    if distance <=100:
        return 10
    elif distance>100 and distance<=500:
        return 8
    elif distance>500 and distance<=2000:
        return 4
    else:
        return 2
