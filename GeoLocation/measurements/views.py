from django.shortcuts import render,get_object_or_404
from .models import Measurement
from .forms import MeasurementModelForm
from geopy.geocoders import Photon
from geopy.distance import geodesic
from .utils import get_geo,get_center_cordinates,get_zoom,get_ip_address
import folium

# Create your views here.

def calculate_distance_view(request):
    distance=None
    destination=None
    obj= get_object_or_404(Measurement,id=1)
    form=MeasurementModelForm(request.POST or None)
    geoloactor = Photon(user_agent='measurements')
    #get_ip_address won't work for localhost this may work in cloud
    #in this case i prefer to use a random ip found in google
    #ip = get_ip_address(request)
    ip='103.138.202.16'
    print(ip)
    country, city, lat, lon = get_geo(ip)
    print(country)
    location = geoloactor.geocode(city)
    #print('###',location)
    pointA=(lat,lon)
    #initial folium map
    m = folium.Map(width=800,height=500,location=get_center_cordinates(lat,lon),zoom_start=8)
    #location marker
    folium.Marker([lat,lon],tooltip='click here for more', popup=city['city'] , icon=folium.Icon(color='purple')).add_to(m)


    if form.is_valid():
        instance = form.save(commit=False)
        destination_ = form.cleaned_data.get('destination')
        destination = geoloactor.geocode(destination_)
        #print(destination)
        d_lat=destination.latitude
        d_lon=destination.longitude
        pointB=(d_lat,d_lon)
        distance = round(geodesic(pointA,pointB).km,2)
        #map modification
        #initial folium map
        m = folium.Map(width=800,height=500,location=get_center_cordinates(lat,lon,d_lat,d_lon),zoom_start=get_zoom(distance))
        #location marker
        folium.Marker([lat,lon],tooltip='click here for more', popup=location , icon=folium.Icon(color='purple')).add_to(m)
        #destination marker
        folium.Marker([d_lat,d_lon],tooltip='click here for more', popup=destination , icon=folium.Icon(color='red',icon='cloud')).add_to(m)

        #draw the line between location and destination
        line = folium.PolyLine(locations=[pointA,pointB],weight=2,color="green")
        m.add_child(line)

        instance.location = location
        instance.distance= distance
        instance.save()

    m = m._repr_html_()




    context={
    'distance':distance,
    'destination':destination,
    'form':form,
    'map':m,
    }
    return render(request,'measurements/main.html',context=context)
