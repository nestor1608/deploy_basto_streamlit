import datetime
import pandas as pd

df_gps= pd.read_csv('csv/data_clean_gps.csv',index_col='Unnamed: 0')
df_gps.createdAt=pd.to_datetime(df_gps.createdAt) 
df_gps.updatedAt=pd.to_datetime(df_gps.updatedAt)



def setle_clean():
    setle_n= pd.read_csv('csv/settle.csv') 
    setle_n = setle_n[['_id','hectares','name','latitud_c','longitud_c']]
    return setle_n

def selec_setle(data,select):
    df_setle = data[data._id== select]
    return df_setle

def animl_clean():
    animal_n= pd.read_csv('csv/data_animals.csv')
    return animal_n

def selec_anim(data,select):
    df_anim= data[data._id==select]
    return df_anim
# def count_register_week(data):
#     week_x= data.groupby(['UUID',data.createdAt.dt.week]).agg({'createdAt':'count'}).rename(columns={'createdAt':'count_register'})
#     week_x=week_x.reset_index()
#     return week_x


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