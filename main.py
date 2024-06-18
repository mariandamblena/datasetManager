import streamlit as st
import pandas as pd
import plotly.express as px

# Título de la aplicación
st.title("Visualización Interactiva de Datos Excel")

# Subir el archivo Excel
uploaded_file = st.file_uploader("Elige un archivo Excel", type="xlsx")

if uploaded_file is not None:
    # Leer el archivo Excel
    df = pd.read_excel(uploaded_file, header=0)  # header=0 indica que la primera fila son los encabezados
    
    # Mostrar el dataframe
    st.write("Datos del archivo Excel:")
    st.write(df)
    
    # Asegurarse de que el DataFrame tiene una columna de fecha y hora
    date_column = st.selectbox("Selecciona la columna de fecha y hora", df.columns)
    df[date_column] = pd.to_datetime(df[date_column], unit='d', origin='1899-12-30')  # Ajuste para convertir la fecha en el formato correcto
    
    # Selección de rango de fecha y hora
    min_date = df[date_column].min()
    max_date = df[date_column].max()
    start_date = st.date_input("Fecha de inicio", min_date)
    end_date = st.date_input("Fecha de fin", max_date)
    start_time = st.time_input("Hora de inicio", min_date.time())
    end_time = st.time_input("Hora de fin", max_date.time())
    
    start_datetime = pd.to_datetime(f"{start_date} {start_time}")
    end_datetime = pd.to_datetime(f"{end_date} {end_time}")
    
    # Filtrar el DataFrame por el rango de fecha y hora seleccionado
    mask = (df[date_column] >= start_datetime) & (df[date_column] <= end_datetime)
    df_filtered = df[mask]
    
    # Mostrar el dataframe filtrado
    st.write("Datos filtrados del archivo Excel:")
    st.write(df_filtered)
    
    # Selección de columnas para graficar
    columns = df.columns.tolist()
    x_axis = st.selectbox("Selecciona la columna para el eje X", columns)
    
    # Selección de múltiples columnas para el eje Y
    y_axes = st.multiselect("Selecciona las columnas para el eje Y", columns)
    
    # Filtrar valores no numéricos en las columnas seleccionadas
    for y_axis in y_axes:
        df_filtered = df_filtered[pd.to_numeric(df_filtered[y_axis], errors='coerce').notnull()]
        df_filtered[y_axis] = df_filtered[y_axis].astype(float)

    # Graficar usando Plotly Express
    st.write("Gráfico con Plotly Express:")
    fig_plotly = px.line(df_filtered, x=x_axis, y=y_axes, title="Variables vs Tiempo", labels={"value": "Valor", "variable": "Variable"})
    st.plotly_chart(fig_plotly)
    
    # Mostrar estadísticas para cada columna Y seleccionada
    for y_axis in y_axes:
        st.write(f"Estadísticas de {y_axis}:")
        st.write(f"Promedio: {df_filtered[y_axis].mean()}")
        st.write(f"Mediana: {df_filtered[y_axis].median()}")
        st.write(f"Desviación estándar: {df_filtered[y_axis].std()}")
        st.write(f"Máximo: {df_filtered[y_axis].max()}")
        st.write(f"Mínimo: {df_filtered[y_axis].min()}")


