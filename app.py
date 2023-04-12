import streamlit as st
import pandas as pd
from suport_st import grafic_map,mapbox_access_token
import plotly.graph_objects as go
import plotly.express as px
from funciones_app import setle_lat,setle_lng,area_perimetro,filter_time_day,interview_vaca,gps_data,data_devices,week_data_filter
from conect_datarows import setle_clean,selec_setle,count_register_week


setle= setle_clean()# arroja dataframe arreglado de setle---

st.title('Hola prueba')

st.dataframe(setle,use_container_width=True)

select_sl= st.selectbox('Seleccione un asentamiento',setle._id.values)
elec_setle= selec_setle(setle,select_sl) # arroja dataframe pequeño de un solo dato del asentamiento---

on_perimetro=area_perimetro(elec_setle.latitud_c, elec_setle.longitud_c, elec_setle.hectares)# arroja dataframe---
uuid_devis = on_perimetro.UUID.values 

select=st.selectbox("seleccionar collar",uuid_devis)
dt_vaca=  data_devices(on_perimetro,select)

moment_day=['madrugada','mañana','tarde','noche']
time_day=st.slider('Selecione momento del dia',0,len(moment_day)-1,0)
st.write(moment_day[time_day])

fi_time= filter_time_day(dt_vaca,moment_day[time_day])
data_week=count_register_week(fi_time)
fig= px.bar( data_week,x='createdAt',y='count_register')
st.plotly_chart(fig,use_container_width=True) 

week= st.slider('Selecione semana',data_week['createdAt'].min() ,data_week['createdAt'].max(),1)

val_vaca= interview_vaca(fi_time)

time_week= week_data_filter(fi_time,'2023-02-14')

if st.button('Recorrido en Mapa'):
    fig = go.Figure()
    grafic_map(fi_time,[select],setle_lat,setle_lng,fig)
    fig.update_layout(
        mapbox=dict(
            style='satellite', # Estilo de mapa satelital
            accesstoken=mapbox_access_token,
            zoom=12, # Nivel de zoom inicial del mapa
            center=dict(lat=elec_setle.latitud_c.values[0] , lon=elec_setle.longitud_c.values[0]),
        ),
        showlegend=False
    )
    st.plotly_chart(fig)


fig=px.line(val_vaca[0])
st.plotly_chart(fig,use_container_width=True) 
st.write(f'Movimiento promedio durante {moment_day[time_day]} de  {pd.Series(val_vaca[0]).mean().round(3) } km')
st.write(f'Distancia recorrida: {pd.Series(val_vaca[0]).sum().round(3)} km')
st.write(f'Tiempo: {pd.Series(val_vaca[2]).sum().round(3)} ')
fig=px.line(val_vaca[1])
st.plotly_chart(fig,use_container_width=True) 
st.write(f'Velocidad promedio {pd.Series(val_vaca[1]).mean().round(3)} /h')
fig=px.line(val_vaca[2])
st.plotly_chart(fig,use_container_width=True) 
st.write(f'Tiempo promedio:  {pd.Series(val_vaca[2]).mean().round(3)} hrs')

