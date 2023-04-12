import pandas as pd
from conect_datarows import df_gps
import plotly.graph_objects as go
from funciones_app import data_devices, gps_data
import seaborn as sns
import matplotlib.colors as mcolors
import random



def random_color():
    """Genera un color cálido aleatorio en formato hexadecimal."""
    n = random.randint(2,100)
    paleta= sns.color_palette("deep",n_colors=n)
    colores_hex = [mcolors.rgb2hex(color) for color in paleta]
    return colores_hex[random.randint(1,n-1)]

df_gps=df_gps

mapbox_access_token = 'pk.eyJ1IjoibmVzdG9yMTYwOCIsImEiOiJjbGc5b2J2d3gwOHgwM2xwamd3cGE4cmExIn0.bPWyeRa73WyNqm1nBNJOvQ' 

def uni_graf(data,color,fig):

    fig.add_trace(go.Scattermapbox(
        lat=data.dataRowData_lat.values,
        lon=data.dataRowData_lng.values,
        mode='lines+markers',
        line=dict(
            width=2,
            color=color,
        ),
        marker=go.scattermapbox.Marker(
            size=8,
            color=color,
            symbol='circle'
        ),
    ))
    return fig

def grafic_map(data,list_vacas,lat_orig,lng_orig,fig):
    colores=[]
    for i in list_vacas:
        color = random_color()
        colores.append(color)
        while color in colores:
            color =random_color()
        dta=data_devices(data, i )
        dta_gps= gps_data(dta)
        uni_graf(dta_gps,color,fig)
        
    fig.update_layout(
        mapbox=dict(
            style='satellite', # Estilo de mapa satelital
            accesstoken=mapbox_access_token,
            zoom=14, # Nivel de zoom inicial del mapa
            center=dict(lat=lat_orig,lon=lng_orig),
        ),
        showlegend=False
    )
    return fig