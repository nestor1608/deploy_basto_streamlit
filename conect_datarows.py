
import pandas as pd

df_gps= pd.read_csv('data_clean_gps.csv',index_col='Unnamed: 0')
df_gps.createdAt=pd.to_datetime(df_gps.createdAt) 
df_gps.updatedAt=pd.to_datetime(df_gps.updatedAt)



def setle_clean():
    setle_n= pd.read_csv('settle.csv') 
    setle_n = setle_n[['_id','hectares','name','latitud_c','longitud_c']]
    return setle_n

def selec_setle(data,select):
    df_setle = data[data._id== select]
    return df_setle

def count_register_week(data):
    week_x= data.groupby(['UUID',data.createdAt.dt.week]).agg({'createdAt':'count'}).rename(columns={'createdAt':'count_register'})
    week_x=week_x.reset_index()
    return week_x