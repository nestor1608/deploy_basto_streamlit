import streamlit as st
import pandas as pd
from suport_st import grafic_map,mapbox_access_token
import plotly.graph_objects as go
import plotly.express as px
from funciones_app import setle_lat,setle_lng,area_perimetro,filter_time_day,interview_vaca,data_devices,week_data_filter
from conect_datarows import setle_clean,selec_setle,obtener_fecha_inicio_fin
import datetime


st.title('Consulta de status')

st.write('A continuación se pueden observar los diferentes perímetros a consultar a partir de los datos proveídos:')


setle= setle_clean()# arroja dataframe arreglado de setle---


st.dataframe(setle,use_container_width=True)


st.write('Favor de aplicar los filtros necesarios para su consulta:')

select_sl= st.selectbox('Seleccione un asentamiento',setle.name.unique())
nombre= setle[setle.name==select_sl]._id.values[0]
print(nombre)
elec_setle= selec_setle(setle,nombre) # arroja dataframe pequeño de un solo dato del asentamiento---

on_perimetro=area_perimetro(elec_setle.latitud_c, elec_setle.longitud_c, elec_setle.hectares)# arroja dataframe---
uuid_devis = on_perimetro.UUID.unique()

select=st.selectbox("Ahora seleccione un collar",uuid_devis)
dt_vaca=  data_devices(on_perimetro,select)


st.write('Visualización de los registros obtenidos a lo largo del tiempo de ese collar en esa locaclización en específica:')


dt_vaca.createdAt= pd.to_datetime(dt_vaca.createdAt)
data_week= dt_vaca.groupby(['UUID',dt_vaca.createdAt.dt.week]).agg({'createdAt':'count'}).rename(columns={'createdAt':'count_register'})
data_week=data_week.reset_index()


st.write('Ahora puede observar una semana en específica con el menú siguiente:')

fig= px.bar( data_week,x='createdAt',y='count_register')
st.plotly_chart(fig,use_container_width=True) 
week= st.slider('Selecione semana',int(data_week['createdAt'].min()) ,int(data_week['createdAt'].max()) )

st.write('En esa semana específica, puede visualizar los datos de un momento específico del día y sus datos de ese collar en específico: Madrugada(0), Mañana(1), Tarde(2), Noche(3)')

moment_day=['madrugada','mañana','tarde','noche']
time_day=st.slider('Selecione momento del dia',0,len(moment_day)-1,0)
time_week= week_data_filter(dt_vaca,week)
fi_time= filter_time_day(time_week,moment_day[time_day])

try:
    date_week= obtener_fecha_inicio_fin(time_week.iloc[-1][['createdAt']].values[0])
    st.subheader(f'Fecha de Inicio: {date_week[0]}')
    st.subheader(f'Fecha de fin: {date_week[1]}')
except IndexError:
    st.warning('No hay datos para estos momento del dia')

st.subheader(moment_day[time_day].upper())



val_vaca= interview_vaca(fi_time)

print(fi_time.shape)
if st.button('Recorrido en Mapa') or fi_time.shape[0]==1:
    fig = go.Figure()
    grafic_map(fi_time,[select],fi_time.iloc[0]['dataRowData_lat'],fi_time.iloc[0]['dataRowData_lng'],fig)
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

if fi_time.shape[0]!=0:
    try:
        if fi_time.shape[0]>1:
            fig=px.line(val_vaca[0])
            st.plotly_chart(fig,use_container_width=True) 
        st.write(f'**Movimiento promedio** durante{moment_day[time_day]} de  {pd.Series(val_vaca[0]).mean().round(3)}km')
        st.write(f'**Distancia recorrida:** {pd.Series(val_vaca[0]).sum().round(3)} km')
        st.write(f'**Tiempo:** {pd.Series(val_vaca[2]).sum().round(3)} ')
        fig=px.line(val_vaca[1])
        st.plotly_chart(fig,use_container_width=True) 
        st.write(f'**Velocidad promedio** {pd.Series(val_vaca[1]).mean().round(3)} k/h')
        fig=px.line(val_vaca[2])
        st.plotly_chart(fig,use_container_width=True) 
        st.write(f'**Tiempo promedio:**  {pd.Series(val_vaca[2]).mean().round(3)} hrs')
    except AttributeError:
        st.table(fi_time[['dataRowData_lng','dataRowData_lat' ]])
else:
    st.warning('No hay registro con estos parametros')
