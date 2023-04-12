from geopy.distance import great_circle
from geopy import Point
import geopandas as gpd
from shapely.geometry import Point
from conect_datarows import df_gps
import math
import pandas as pd
import datetime
"""funcion que puede arrojar la distancia[0], velocidad promedio[1], timepo que llevo el recorrido [2] recorrida entre el primer punto de la lista y el ultimo los datos tiene que ser solo gps.. hya otra funcion que la complemeta para limpiar estos datos """
def distancia_recorrida(data):
    cordena1=tuple(data.iloc[0][['dataRowData_lat','dataRowData_lng']].values)
    cordena2= tuple(data.iloc[-1][['dataRowData_lat','dataRowData_lng']].values)
    dista_km= great_circle(cordena1,cordena2).kilometers
    return dista_km


def interview_vaca(data): # tratar de filtrar por perimetro porque si hay valores (que los hay)fuera de rango de los -90 90 da error
    data_dis=[]
    data_vel=[]
    data_time=[]
    for i in range(0,data.shape[0]+1):
        try:
            dista_km= great_circle(tuple(data.iloc[i][['dataRowData_lat','dataRowData_lng']].values),tuple(data.iloc[i+1][['dataRowData_lat','dataRowData_lng']].values)).kilometers
            if dista_km <= 8.:
                data_dis.append(round(dista_km,3))
            if data.iloc[i].dataRowData_gpsVel:
                data_vel.append(round(data.iloc[i].dataRowData_gpsVel,3))
                data_time.append(round(dista_km/data.iloc[i].dataRowData_gpsVel,3))
            else:
                data_time.append(round(dista_km/pd.Series(data_vel).mean(),3))# les puede dar error si el array de velocidad esta vacio... toma el valor promedio de las velocidades que hay hasta el momento
        except IndexError:
            pass
    return data_dis,data_vel,data_time


setle_lat=-34.163851
setle_lng=-64.071678

gdf= gpd.GeoDataFrame(df_gps,crs='EPSG:4326',geometry=gpd.points_from_xy(df_gps.dataRowData_lng,df_gps.dataRowData_lat))



def perimetro_aprox(hectarea):
    """Funcion: funcion que saca el numero(float) del radio de un perimetra en kilometros
    Returns:
        _type_: float valor en kilometros del radio de un perimetro
    """
    hect=hectarea
    lado = math.sqrt(hect)*10
    perim = lado*4
    return perim

def area_perimetro(latitud,longitud,hectareas):
    """Funcion que genera un dataframe nuevo a partir de un un punto latitud longitud y la cantidad de hectareas fitra ese perimetro

    Args:
        latitud (gps): latitud de punto central
        longitud (gps): longitud de punto central
        hectareas (float): numero de hectareas que posee el terreno

    Returns:
        _type_: dataframe filtrado dentro de un perimetro generado
    """
    setle_lat=latitud
    setle_lng=longitud
    punto_referencia= Point(setle_lng,setle_lat)	
    per_kilo= perimetro_aprox(hectareas)
    circulo= punto_referencia.buffer(per_kilo/111.32) # valor 1 grado aprox en kilometro en el ecuador 
    on_perimetro= gdf[gdf.geometry.within(circulo)]
    return on_perimetro


def data_devices(data,uuid):
    data=data[data.UUID==uuid]
    return data

def gps_data(data):
    gps= data[['dataRowData_lat','dataRowData_lng']]
    gps = gps.dropna()
    return gps


def obtener_fecha_inicio_fin(semana):
    """
    Función que recibe una semana en formato de fecha y devuelve la fecha de inicio y finalización de esa semana.
    
    Args:
    semana (str o datetime): Semana en formato de fecha. Debe estar en formato 'YYYY-MM-DD'.
    
    Returns:
    fecha_inicio (str): Fecha de inicio de la semana en formato 'YYYY-MM-DD'.
    fecha_fin (str): Fecha de finalización de la semana en formato 'YYYY-MM-DD'.
    """
    
    if isinstance(semana, str):
        semana = datetime.datetime.strptime(semana, '%Y-%m-%d')
        
    dia_semana = semana.weekday()
    
    fecha_inicio = semana - datetime.timedelta(days=dia_semana)
    fecha_fin = fecha_inicio + datetime.timedelta(days=6)
    
    fecha_inicio = fecha_inicio.strftime('%Y-%m-%d')
    fecha_fin = fecha_fin.strftime('%Y-%m-%d')
    return fecha_inicio, fecha_fin


def filter_time_day(data,momento):
    switch_dict={
        'noche': data[((data.updatedAt.dt.hour > 20) & (data.updatedAt.dt.hour < 24))| ((data.updatedAt.dt.hour > 0) & (data.updatedAt.dt.hour < 7))],
        'madrugada':  data[(data.updatedAt.dt.hour > 0) & (data.updatedAt.dt.hour < 7)],
        'tarde':data[(data.updatedAt.dt.hour > 13) & (data.updatedAt.dt.hour < 20)],
        'mañana':data[(data.updatedAt.dt.hour > 7) & (data.updatedAt.dt.hour < 13)]
    }
    return switch_dict.get(momento,'valor')


def week_data_filter(data,fecha):
    if isinstance(fecha,int):
        data = data[data.createdAt.dt.week == fecha]
    else:
        week = obtener_fecha_inicio_fin(fecha)
        data = data[(data.createdAt >= week[0]) & (data.createdAt <= week[1])]
    return data