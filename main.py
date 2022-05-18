import functions as f
import streamlit as st

def main():
	st.set_page_config(page_title="Cargatron", page_icon=":rocket", layout="wide")
	with st.sidebar:
		option = st.selectbox('Seleccione una opción del menu', ('Home','Data','Map'))
		upload_file = st.file_uploader('Carga tus propios datos', type = 'csv')
	df = f.load_dataframe(upload_file)
	if option == 'Home':
		f.load_home()
	elif option == 'Data':
		with st.echo():
			st.dataframe(df)
	elif option == 'Map':
		col1, col2, col3 = st.columns([1,3,2])
		with col1:
			agree, agree1, df_copy = f.show_filters(df)
		with col2:
			f.show_map(agree, df_copy)
		with col3:
			f.show_charts(agree, agree1, df)

if __name__ == "__main__":
    main()


