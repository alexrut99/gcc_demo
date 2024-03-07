import folium
import pandas as pd
import streamlit as st
import leafmap.foliumap as leafmap
import folium.plugins as plugins
import conversion
import clickmarker
import geopandas as gpd
import matplotlib.pyplot as plt

from folium.plugins import Draw, MousePosition,  MeasureControl, PolyLineOffset, PolyLineTextPath, GroupedLayerControl, FloatImage,Search

st.set_page_config(layout="wide")

st.sidebar.info(
    """
        ## Mr. Anirut Ladawadee 
        Hydro-Geologist 
        Department of Groundwater Resource, Thailand.  I have been conducting study projects 
        related to land subsidence groundwater monitoring, database management. Recently, 
        He has started to work in the field of Geographical Based Management Information System 
        for Groundwater Management in the Groundwater Critical Zone, Groundwater Quality Conservation 
        and Protection, Groundwater Quality Assessment, Contamination	Monitoring System in Thailand
    """
)

st.sidebar.title("Contact")
st.sidebar.info(
    """
    Anirut Ladawadee: anirut577@gmail.com
    """
)


st.title("MapView")
# df = pd.read_csv("data/scotland_xyz.tsv", sep="\t")
basemaps = leafmap.basemaps
names = list(basemaps.keys())
links = list(basemaps.values())

col1, col2, col3, col4, col5, col6= st.columns([3, 1, 1, 3, 3, 1.5])

m = leafmap.Map(
    center=[13.840313, 100.571176],
    zoom=10,
    locate_control=True,
    draw_control=False,
    measure_control=False,
)
#selectbox
with col1:
    
    option = st.selectbox("เลือกระบบพิกัด" ,
                      ("UTM" , "LAT/LONG" ))
if option == "UTM":
        
    with col4:
        # lat = st.slider('Latitude', -90.0, 90.0, 12.92 step=0.01)
        utme = st.number_input("UTME",150000,850000, 669808 ) 
    with col5:
        # lon = st.slider('Longitude', -180.0, 180.0, 101.42, step=0.01)
        utmn = st.number_input("UTMN",0,2300000,1530623)
    with col2:
        # lat = st.slider('Latitude', -90.0, 90.0, 12.92 step=0.01)
        zone_n = st.number_input("Zone",1,60,47) 
    with col3:
        # lon = st.slider('Longitude', -180.0, 180.0, 101.42, step=0.01)
        zone_l = st.text_input("", "P")
        
    con = conversion.to_latlon(int(utme),int(utmn),zone_n,zone_l)
    lat = con[0]
    lon = con[1]

    m = leafmap.Map(
    center=[float(lat), float(lon)],
    # zoom=int(zoom),
    zoom=18,
    locate_control=True,
    # draw_control=False,
    measure_control=False,
)
    folium.Marker(
    location=[float(lat), float(lon)],
    # tooltip="Click me!",
    popup= (utme, utmn),
    icon=folium.Icon(color="red"),
).add_to(m)
    
elif option == "LAT/LONG":
    
    with col4:
    # lat = st.slider('Latitude', -90.0, 90.0, 12.92 step=0.01)(13.840313975778361, 100.57117601875181)
        lat = st.text_input("Latitude","13.840313") 

    with col5:
        # lon = st.slider('Longitude', -180.0, 180.0, 101.42, step=0.01)
        lon = st.text_input("Longitude","100.571176" )
        
    m = leafmap.Map(
    center=[float(lat), float(lon)],
    # zoom=int(zoom),
    zoom=18,
    locate_control=True,
    # draw_control=False,
    measure_control=False,
)
    folium.Marker(
    location=[float(lat), float(lon)],
    # tooltip="Click me!",
    popup= (lat, lon), 
    # popup= "https://www.google.com/maps?layer=c&cbll=' + lat + ',' + long + '",
    
    icon=folium.Icon(color="red"),
).add_to(m)
    
with col1:
    right_name = st.selectbox(
        "Select layer",
        names,
        index=names.index("HYBRID"),
    )


    


if right_name in basemaps:
    right_layer = basemaps[right_name]
else:
    right_layer = folium.TileLayer(
        tiles=links[names.index(right_name)],
        name=right_name,
        
        overlay=True,
    )
    


measure = plugins.MeasureControl(position="bottomleft", active_color="red")
measure.add_to(m)

fmtr = "function(num) {return L.Util.formatNum(num, 3) + '  ';};"
plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",
                      lat_formatter=fmtr, lng_formatter=fmtr).add_to(m)



df1 = pd.read_excel('./data/bkk_gov.xlsx', sheet_name='Sheet1')

gdf1 = gpd.GeoDataFrame(
    df1, geometry=gpd.points_from_xy(df1.utme.astype(float), df1.utmn.astype(float)), crs="EPSG:32647",
    )

df2 = pd.read_csv("./data/private_well.csv")

gdf2 = gpd.GeoDataFrame(
    df2, geometry=gpd.points_from_xy(df2.Easting.astype(float), df2.Northing.astype(float)), crs="EPSG:32647",
)



# fg1 = folium.FeatureGroup(name='ท่อประปา', show=False)
fg2 = folium.FeatureGroup(name='บ่อบาดาลราชการ', show=False)
fg3 = folium.FeatureGroup(name='บ่อบาดาลเอกชน', show=False)
# fg4 = folium.FeatureGroup(name='บ่อน้ำบาดาลเอกชน', show=False)



# folium.GeoJson(
#     "./data/mwa_d.geojson",
#     style_function=lambda feature: {
#         "fillColor": "#ffff00",
#         "color": "yellow",
#         "weight": 2,
#         "dashArray": "5, 5",
#     },
# ).add_to(fg1)


folium.GeoJson(
    gdf1,
    name="บ่อบาดาลราชการ",
    marker=folium.CircleMarker(radius=6, fill_color="yellow", fill_opacity=0.4, color="black", weight=3),
    tooltip=folium.GeoJsonTooltip(fields=["หมายเลขบ่อน้ำบาดาล", "สถานะที่เจาะ", "ความลึกพัฒนา", "ปริมาณน้ำ"]),
    popup=folium.GeoJsonPopup(fields=["หมายเลขบ่อน้ำบาดาล", "สถานะที่เจาะ", "ความลึกพัฒนา", "ปริมาณน้ำ"]),
    style_function=lambda x: {
        "fillColor": "blue",
        "color": "yellow"
        # "radius": (x['properties']['ขนาด'])*30,
    },
    highlight_function=lambda x: {"fillOpacity": 0.8},
    zoom_on_click=True,
).add_to(fg2)

folium.GeoJson(
    gdf2,
    name="บ่อบาดาลเอกชน",
    marker=folium.CircleMarker(radius=6, fill_color="yellow", fill_opacity=0.4, color="black", weight=3),
    tooltip=folium.GeoJsonTooltip(fields=["หมายเลขบ่อ", "วัตถุประสงค์", "ขนาด", "ลึกถึง"]),
    popup=folium.GeoJsonPopup(fields=["หมายเลขบ่อ", "วัตถุประสงค์", "ขนาด", "ลึกถึง"]),
    style_function=lambda x: {
        "fillColor": "red",
        "color": "orange"
        # "radius": (x['properties']['ขนาด'])*30,
    },
    highlight_function=lambda x: {"fillOpacity": 0.8},
    zoom_on_click=True,
).add_to(fg3)





# m.add_child(fg1)
m.add_child(fg2)
m.add_child(fg3)
# m.add_child(fg4)

click_for_marker = clickmarker.ClickForOneMarker()
m.add_child(click_for_marker)


m.add_basemap(right_name) 
m.to_streamlit(height=600)

# streamlit run streamlit_app.py
