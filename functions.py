import streamlit as st
import pandas as pd

def load_dataframe(upload_file):
	url = 'data/red_recarga_acceso_publico_2021.csv'
	df = pd.read_csv(url, sep=';')
	df = df.rename({'latidtud':'latitude', 'longitud':'longitude'}, axis=1)
	if upload_file is not None:
		df = pd.read_csv(upload_file)
	return df

def load_home():
	st.balloons()
	st.title('CARGATRON')
	st.subheader('By: Paris Martínez Ruiz')
	st.image('img/puntos-recarga-madrid.jpg')
	with st.expander("Ver más"):
		st.write("""
			Aplicación que nos permita localizar las diferentes
			estaciones de carga de coches eléctricos que hay en Madrid.
		""")

def show_filters(df):
	df_copy = df.copy()
	distrito = st.selectbox('Seleccione una opción del menu', (df_copy.DISTRITO.unique()))
	operador = st.selectbox('Seleccione una opción del menu', (df_copy.OPERADOR.unique()))
	cantidad = st.select_slider('Seleccionar nº de cargadores', range(df_copy['Nº CARGADORES'].min(), df_copy['Nº CARGADORES'].max()+1))

	agree = st.checkbox('Filtrar por distrito')
	if agree:
		df_copy = df_copy[df_copy.DISTRITO == distrito]
	agree1 = st.checkbox('Filtrar por Operador')
	if agree1:
		df_copy = df_copy[df_copy.OPERADOR == operador]
	agree2 = st.checkbox('Filtrar por nº de cargadores')
	if agree2:
		df_copy = df_copy[df_copy['Nº CARGADORES'] >= cantidad]

	if df_copy.empty:
		st.warning('¡No hay resultados!')
		st.stop()
	return agree, agree1, df_copy

def show_map(agree, df_copy):
	# st.dataframe(df_copy)
	df_map = df_copy.loc[:,['longitude','latitude']]
	if agree:
		st.map(df_map, zoom=13)
	else:
		st.map(df_map, zoom=11)

def show_charts(agree, agree1, df):
	if agree == False:
		chart_distrito = df.groupby('DISTRITO')['Nº CARGADORES'].sum()
		st.subheader('Nº de cargadores por distrito')
		st.bar_chart(chart_distrito)
	if agree1 == False:
		chart_operador = df.groupby('OPERADOR')['Nº CARGADORES'].sum()
		st.subheader('Nº de cargadores por operador')
		st.bar_chart(chart_operador)
	chart_cargadores = df.groupby('Nº CARGADORES')['OPERADOR'].count()
	st.bar_chart(chart_cargadores)
