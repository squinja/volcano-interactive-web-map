import folium
import pandas

#HTML Formatting
html = """<h4>Volcano Information:</h4>
Name: %s<br><br>
Location: %s<br><br>
Status: %s<br><br>
Height: %s meters<br><br>
Type: %s<br><br>
<a href = "https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a>
"""

map = folium.Map(location=[36.00245155606482, -118.56719979095456], zoom_start = 6)

#Set up feature groups for layer control
ftgroup_volcano = folium.FeatureGroup(name="Volcanoes")
ftgroup_population = folium.FeatureGroup(name="Population")

#Extract from csv and assign each column to list
df = pandas.read_csv('Volcanoes.txt', sep=',')
name = list(df["NAME"])
location = list(df["LOCATION"])
status = list(df["STATUS"])
elevation = list(df["ELEV"])
typeX = list(df["TYPE"])
lat = list(df["LAT"])
lon = list(df["LON"])

#Distinguish elevation based on height
def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 2000:
        return 'orange'
    elif elevation > 2000:
        return 'red'

#Create icon to draw to layer
for lt, ln, na, loc, stat, elev, typ in zip(lat,lon, name, location, status, elevation, typeX): 

    iframe = folium.IFrame(html=html % (na, loc, stat, elev, typ, na, na), width=200, height=200)

    ftgroup_volcano.add_child(folium.CircleMarker(location=[lt,ln], radius = 12, popup=folium.Popup(iframe), tooltip=na, fillColor = color_producer(elev), color = color_producer(elev), fill=True, fillOpacity=0.7))

#Adds colors according to country population
ftgroup_population.add_child(folium.GeoJson(data=open('world.json', 'r', encoding="utf-8-sig").read(), style_function = lambda x: {'fillColor': 'green' if x['properties']['POP2005'] < 1000000 else 'yellow' if 1000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))




#Assign feature groups to map
map.add_child(ftgroup_volcano)
map.add_child(ftgroup_population)


#Layer control
map.add_child(folium.LayerControl())

#Create the html file
map.save("Map1.html")