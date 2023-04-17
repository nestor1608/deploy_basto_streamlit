import streamlit as st
import pandas as pd
from suport_st import grafic_map,mapbox_access_token
import plotly.graph_objects as go
import plotly.express as px
from funciones_app import filter_area_perimetro,filter_time_day,data_devices,week_data_filter,aguada,dataframe_interview_vaca
from conect_datarows import setle_clean,selec_setle,obtener_fecha_inicio_fin,df_gps


setle= setle_clean()# arroja dataframe arreglado de setle---

st.title('Hola prueba')

st.dataframe(setle,use_container_width=True)

select_sl= st.selectbox('Seleccione un asentamiento',setle.name.unique())
nombre = setle[setle.name== select_sl]._id.values[0]
elec_setle= selec_setle(setle,nombre) # arroja dataframe pequeño de un solo dato del asentamiento---

on_perimetro=filter_area_perimetro(df_gps,elec_setle.latitud_c, elec_setle.longitud_c, elec_setle.hectares)# arroja dataframe---
if on_perimetro.shape[0]!=0:
    # agua = aguada(on_perimetro)
    # on_perimetro = on_perimetro.drop(on_perimetro[on_perimetro['UUID'] == agua.loc[0,'UUID']].index)
    uuid_devis = on_perimetro.UUID.unique()

    select=st.selectbox("seleccionar collar",uuid_devis)
    dt_vaca=  data_devices(on_perimetro,select)
    dt_vaca.createdAt= pd.to_datetime(dt_vaca.createdAt)

    data_week= dt_vaca.groupby(['UUID',dt_vaca.createdAt.dt.week]).agg({'createdAt':'count'}).rename(columns={'createdAt':'count_register'})
    data_week=data_week.reset_index()


    if int(data_week['createdAt'].min())!= int(data_week['createdAt'].max()):
        fig= px.bar( data_week,x='createdAt',y='count_register')
        st.plotly_chart(fig,use_container_width=True)
        week= st.slider('Selecione semana',int(data_week['createdAt'].min()) ,int(data_week['createdAt'].max()) )



    moment_day=['madrugada','mañana','tarde','noche']
    time_day=st.select_slider('Selecione momento del dia',options=moment_day)

    time_week= week_data_filter(dt_vaca,week)
    fi_time= filter_time_day(time_week,time_day)

    sep_time=time_week.groupby(time_week.createdAt.dt.date).agg({'UUID':'count'}).rename(columns={'UUID':'count_register'}).reset_index().rename(columns={'createdAt':'day'})
    sep_time.day= pd.to_datetime(sep_time.day)

    day=sep_time.day.dt.date.values

    day_select=st.select_slider('Seleccionar dia',options=day)
    fig=px.bar(sep_time,x=sep_time.day.dt.day_name(), y=sep_time.count_register)
    st.plotly_chart(fig,use_container_width=True) 

    try:
        date_week= obtener_fecha_inicio_fin(time_week.iloc[-1][['createdAt']].values[0])
        st.subheader(f'Fecha de Inicio: {date_week[0]}')
        st.subheader(f'Fecha de fin: {date_week[1]}')
    except IndexError:
        st.warning('No hay datos para estos momento del dia')

    st.subheader(time_day.upper())



    val_vaca= dataframe_interview_vaca(fi_time)


    if st.button('Recorrido en Mapa') or fi_time.shape[0]==1:
        fig = go.Figure()
        grafic_map(fi_time,[select], fi_time.iloc[0]['dataRowData_lat'], fi_time.iloc[0]['dataRowData_lng'], fig, aguada(on_perimetro))
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
                fig=px.line(val_vaca['distancia'])
                st.plotly_chart(fig,use_container_width=True)
            mean_dist, dist_sum =val_vaca[['distancia']].mean().round(3),val_vaca['distancia'].sum().round(3)
            sum_tim, time_mean= val_vaca['tiempo'].sum().round(3),val_vaca['tiempo'].mean().round(3)
            velo_mean=val_vaca['tiempo'].mean().round(3)
            st.write(f'Movimiento promedio durante {time_day} de  {mean_dist}km')
            st.write(f'Distancia recorrida: {dist_sum} km')
            st.write(f'Tiempo: {sum_tim} ')
            fig=px.area(val_vaca,x=val_vaca.point_ini,y=val_vaca['velocidad'])
            st.plotly_chart(fig,use_container_width=True) 
            st.write(f'Velocidad promedio {velo_mean} k/h')
            fig=px.line(val_vaca['tiempo'])
            st.plotly_chart(fig,use_container_width=True) 
            st.write(f'Tiempo promedio:  {time_mean} hrs')
        except AttributeError:
            st.table(fi_time[['dataRowData_lng','dataRowData_lat' ]])
    else:
        st.warning('No hay registro con estos parametros')

    st.dataframe(val_vaca)
else:
    st.warning('Lugar sin dato')