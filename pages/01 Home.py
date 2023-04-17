import streamlit as st
import pandas as pd
from suport_st import grafic_map,mapbox_access_token
import plotly.graph_objects as go
import plotly.express as px
from funciones_app import filter_time_day,interview_vaca,data_devices,week_data_filter, filter_area_perimetro
from conect_datarows import setle_clean,selec_setle,obtener_fecha_inicio_fin, animl_clean, df_gps
import datetime
import streamlit_analytics
import plotly.express as px

st.image('imagenes/Header_bastó.jpeg')

st.title('Información general')

st.write('Gracias a la base de datos podemos saber el conteo de animales en el sigue menú.')

animals= animl_clean()
setle= setle_clean()# arroja dataframe arreglado de setle---


#st.dataframe(animals,use_container_width=True)

select_an= st.selectbox('Seleccione tipo de animal:',animals.animalType.unique())
#selec_an= select_an(animals, ) # arroja dataframe pequeño de un solo dato del asentamiento---



df=animals[animals['animalType']==select_an]
a= df['animalType'].count()
b= animals['animalType'].count()

clicked = st.button("Conteo animales")
if clicked:
    st.write(
        f"En esta área hay: {a}:"
    )
    st.write(
        f"En total hay: {b}"
    )
    st.write('La semana en las que más hubo registros dentro de este potrero fueron de 13 del año. Que comprenden del 20 al 34 de marzo del 2023')
    df.createdAt= pd.to_datetime(df.createdAt)
    data_week= df.groupby(['_id',df.createdAt.dt.week]).agg({'createdAt':'count'}).rename(columns={'createdAt':'count_register'})
    data_week=data_week.reset_index()

    fig= px.bar( data_week,x='createdAt',y='count_register')
    st.plotly_chart(fig,use_container_width=True) 

    #st.write(
        #f"La proporción de {df['animalType']} es: {a*100/b}"
    #)
    #st.write("Para conocer más datos sobre esta población, dé click en la siguiente sección")
 
#datasetrazas= pd.DataFrame(df[['_id','breed']])

clicked_2 = st.button("Más informacion")

if clicked_2:
    st.write(
        f"El peso promedio de esta población es: {df['weight'].mean()}, con una desviación estandar de {df['weight'].std()}"

    )
    st.write(
        f"Las razas registradas son: {pd.DataFrame(df['breed'].value_counts())} "
    )
    #peso= df['weight']
    #conteo= df['_id']
    #data_cont= df.groupby(['_id',df.animalType]).agg({'animalType':'count'}).rename(columns={'animalType':'count_register'})

    #fig= px.bar(x=df['weight'],y=data_cont)
    #fig.show()


st.title('Información de Potrero de interés')


select_sl= st.selectbox('Seleccione un asentamiento a evaluar:',setle.name.unique())
nombre= setle[setle.name==select_sl]._id.values[0]
print(nombre)
elec_setle= selec_setle(setle,nombre) # arroja dataframe pequeño de un solo dato del asentamiento---

on_perimetro=filter_area_perimetro(df_gps,elec_setle.latitud_c, elec_setle.longitud_c, elec_setle.hectares)# arroja dataframe---
uuid_devis = on_perimetro.UUID.unique()

clicked_3 = st.button("Conteo dispositivo")
if clicked_3:
    st.write(
        f"En esta área hay: {len(uuid_devis)} collares que proveen datos de GPS de un total de 518 vacas en total"
    )
    

