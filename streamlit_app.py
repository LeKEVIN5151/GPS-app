import streamlit as st
import pynmea2
import folium
from streamlit_folium import st_folium 
import requests
import pandas as pd
from geopy.distance import geodesic
from datetime import datetime
import pydeck as pdk
from PIL import Image

# Menú lateral para elegir la sección
st.sidebar.title("Selecciona el servicio")
opcion = st.sidebar.radio("Servicios", ["Home","Ubicación mediante trama NMEA", "Análisis Simulador de Vuelo", "Ubicación G-STAR IV"])

if opcion == "Home":
    # Cargar imágenes (asegúrate de tener los archivos en la carpeta de tu proyecto o usar una URL)
    logo_universidad = Image.open("images/logounrc_2.png")
    logo_facultad = Image.open("images/logoing.png")

        # Mostrar logos centrados y a la misma altura
    col1, col2, col3, col4 = st.columns([1, 0.1, 0.2, 0.2])  # Crear cuatro columnas de igual ancho

    with col1:
        st.title("Aplicación de Servicios GPS")

    with col3:
        st.image(logo_universidad, width=200, use_container_width=True)
    with col4:
        st.image(logo_facultad, width=200, use_container_width=True)

    with col2:
        st.write(" ")

    st.write("""
        Esta aplicación ofrece diversos servicios relacionados con la ubicación GPS y el análisis de datos de vuelo.
        Desarrollada como parte de un proyecto académico en colaboración con la Facultad de Ingeniería y la Universidad, 
        tiene como objetivo facilitar el acceso a datos geoespaciales en tiempo real.
    """)

    gps = Image.open("images/gps.png")
    st.image(gps, width=1000)

    st.write("""

        ## Alumnos:
        - **Buten Andrés Benjamín**
        - **Demaio Ignacio Laureano**
        - **Haponiuk Kevin**

        **Sistemas de Radionavegación 2024**
    """)

# Sección "Ubicación mediante trama NMEA"
elif opcion == "Ubicación mediante trama NMEA":
    st.header("Ubicación mediante trama NMEA")
    # Entrada de la trama NMEA
    nmea_input = st.text_input("Ingresa la trama NMEA")

    if nmea_input:
        try:
            # Procesamiento de la trama NMEA
            msg = pynmea2.parse(nmea_input)
            latitude = msg.latitude
            longitude = msg.longitude

            # Mostrar los datos procesados
            st.write(f"Latitud: {latitude}")
            st.write(f"Longitud: {longitude}")

            # Mapa
            map_location = folium.Map(location=[latitude, longitude], zoom_start=15)
            folium.Marker([latitude, longitude], tooltip="Ubicación actual").add_to(map_location)

            # Mostrar mapa en Streamlit
            st_folium(map_location, width=900, height=700)

        except Exception as e:
            st.error(f"Error procesando la trama NMEA: {e}")

# Sección "Análisis Simulador de Vuelo"
elif opcion == "Análisis Simulador de Vuelo":
        st.title("Análisis Simulador de Vuelo")
        st.write("Sube un archivo de datos de vuelo en formato .txt")

        # Cargar archivo
        archivo = st.file_uploader("Selecciona un archivo .txt", type="txt")

    # Función para calcular métricas de vuelo
        def calcular_metricas(datos_vuelo):
            # Calcular tiempo total de vuelo
            tiempos = pd.to_datetime(datos_vuelo['Tiempo'], format='%H:%M:%S')
            tiempo_total_minutos = (tiempos.iloc[-1] - tiempos.iloc[0]).total_seconds() / 60

            # Calcular velocidad horizontal promedio
            distancias = [geodesic((datos_vuelo['Lat'][i], datos_vuelo['Long'][i]),
                                (datos_vuelo['Lat'][i+1], datos_vuelo['Long'][i+1])).meters
                        for i in range(len(datos_vuelo) - 1)]
            tiempo_total_segundos = (tiempos.iloc[-1] - tiempos.iloc[0]).total_seconds()
            velocidad_horizontal_promedio = sum(distancias) / tiempo_total_segundos if tiempo_total_segundos > 0 else 0

            # Calcular altitud máxima y mínima
            altitud_maxima = datos_vuelo['AltMSL'].max()
            altitud_minima = datos_vuelo['AltMSL'].min()

            # Calcular velocidad vertical promedio
            altitudes = datos_vuelo['AltMSL'].diff().fillna(0)
            velocidad_vertical_promedio = sum(abs(altitudes)) / tiempo_total_segundos if tiempo_total_segundos > 0 else 0

            # Calcular inclinación promedio y variación (Roll, Pitch, Yaw)
            inclinacion_promedio = (
                datos_vuelo['Roll'].mean(),
                datos_vuelo['Pitch'].mean(),
                datos_vuelo['Yaw'].mean()
            )
            variacion_inclinacion = (
                datos_vuelo['Roll'].std(),
                datos_vuelo['Pitch'].std(),
                datos_vuelo['Yaw'].std()
            )

            # Crear un diccionario con las métricas para mostrar
            metricas = {
                "Tiempo total de vuelo (minutos)": tiempo_total_minutos,
                "Velocidad horizontal promedio (m/s)": velocidad_horizontal_promedio,
                "Altitud máxima (m)": altitud_maxima,
                "Altitud mínima (m)": altitud_minima,
                "Velocidad vertical promedio (m/s)": velocidad_vertical_promedio,
                "Inclinación promedio (Roll, Pitch, Yaw)": inclinacion_promedio,
                "Variación de inclinación (Roll, Pitch, Yaw)": variacion_inclinacion
            }
            return metricas

        if archivo is not None:
            # Leer archivo
            datos_vuelo = pd.read_csv(
                archivo,
                sep=';',
                skiprows=1,
                names=["Tiempo", "Lat", "Long", "AltMSL", "AltRad", "Roll", "Pitch", "Yaw"]
            )

            # Calcular métricas
            metricas = calcular_metricas(datos_vuelo)

            # Mostrar métricas
            st.subheader("Métricas de vuelo")
            st.write(f"**Tiempo total de vuelo (minutos):** {metricas['Tiempo total de vuelo (minutos)']:.2f}")
            st.write(f"**Velocidad horizontal promedio (m/s):** {metricas['Velocidad horizontal promedio (m/s)']:.2f}")
            st.write(f"**Altitud máxima MSL (m):** {metricas['Altitud máxima (m)']:.2f}")
            st.write(f"**Altitud mínima MSL (m):** {metricas['Altitud mínima (m)']:.2f}")
            st.write(f"**Velocidad vertical promedio (m/s):** {metricas['Velocidad vertical promedio (m/s)']:.5f}")
            st.write("**Inclinación promedio (Roll, Pitch, Yaw):** "
                    f"({metricas['Inclinación promedio (Roll, Pitch, Yaw)'][0]:.2f}, "
                    f"{metricas['Inclinación promedio (Roll, Pitch, Yaw)'][1]:.2f}, "
                    f"{metricas['Inclinación promedio (Roll, Pitch, Yaw)'][2]:.2f})")
            st.write("**Variación de inclinación (Roll, Pitch, Yaw):** "
                    f"({metricas['Variación de inclinación (Roll, Pitch, Yaw)'][0]:.2f}, "
                    f"{metricas['Variación de inclinación (Roll, Pitch, Yaw)'][1]:.2f}, "
                    f"{metricas['Variación de inclinación (Roll, Pitch, Yaw)'][2]:.2f})")

            # Mostrar el recorrido en un mapa

            df = pd.DataFrame({
                'lat': datos_vuelo['Lat'],
                'lon': datos_vuelo['Long']
            })

            # Muestra el mapa con puntos más pequeños y de un color personalizado
            st.map(df, size=0.001, color="#0cb8eb")


            datos_vuelo['Tiempo'] = pd.to_datetime(datos_vuelo['Tiempo'], format='%H:%M:%S') #esto es para acomodar en el eje el tiempo, sino queda bien feo vieja


            st.subheader("Altitud (Radioaltímetro) vs. Tiempo")
            # Usamos 'Tiempo' para el eje X y 'AltMSL' para el eje Y
            st.line_chart(data=datos_vuelo.set_index('Tiempo')['AltRad'])


            st.subheader("Altitud (MSL) vs. Tiempo")
            # Asegúrate de que 'Tiempo' esté en formato datetime


            # Usamos 'Tiempo' para el eje X y 'AltMSL' para el eje Y
            st.line_chart(data=datos_vuelo.set_index('Tiempo')['AltMSL'])

            st.subheader("Velocidad vertical vs Tiempo")
            datos_vuelo['Velocidad_Vertical'] = datos_vuelo['AltMSL'].diff().fillna(0)
            st.line_chart(data=datos_vuelo.set_index('Tiempo')['Velocidad_Vertical'])

            st.subheader("Velocidad horizontal vs Tiempo")
            velocidades = [
                geodesic((datos_vuelo['Lat'][i], datos_vuelo['Long'][i]),
                        (datos_vuelo['Lat'][i+1], datos_vuelo['Long'][i+1])).meters
                for i in range(len(datos_vuelo) - 1)
            ]
            velocidades.append(0)
            datos_vuelo['Velocidad_Horizontal'] = velocidades
            st.line_chart(data=datos_vuelo.set_index('Tiempo')['Velocidad_Horizontal'])

            # Crear un DataFrame con los datos de inclinación y tiempo
            chart_data = datos_vuelo[["Tiempo", "Roll", "Pitch", "Yaw"]]

            # Asegurarse de que la columna 'Tiempo' sea un índice adecuado para el gráfico
            chart_data["Tiempo"] = pd.to_datetime(chart_data["Tiempo"], format='%H:%M:%S')
            chart_data.set_index("Tiempo", inplace=True)

            map_data = datos_vuelo[["Lat", "Long", "AltMSL"]]

            # Crear una capa de puntos en 3D
            deckgl_layer = pdk.Layer(
                "PointCloudLayer",
                map_data,
                get_position=["Long", "Lat", "AltRad"],  # Lat, Long, Altitud
                get_radius=0.1,  # Ajusta el tamaño del punto
                get_color=[255, 0, 0],  # Color de los puntos (rojo)
                pickable=True,  # Habilita la selección interactiva de puntos
            )

            # Definir la vista inicial del mapa (en términos de latitud, longitud y zoom)
            view_state = pdk.ViewState(
                latitude=map_data["Lat"].mean(),  # Centrado en el centro del vuelo
                longitude=map_data["Long"].mean(),
                zoom=6,  # Ajusta el zoom inicial
                pitch=200,  # Ángulo de inclinación para el efecto 3D
                bearing=0  # Ángulo de rotación
            )

            # Crear el deck.gl map con la capa 3D y la vista
            r = pdk.Deck(layers=[deckgl_layer], initial_view_state=view_state, tooltip={"text": "{Lat}, {Long}, {AltMSL}"})

            # Mostrar el mapa en Streamlit
            st.pydeck_chart(r)

# Sección "Ubicación G-STAR IV"
elif opcion == "Ubicación G-STAR IV":
    API_URL = "http://0.0.0.0:5000/location"  # Cambia a tu dominio y puerto si necesario

    def obtener_datos_gps():
        try:
            response = requests.get(API_URL)
            if response.status_code == 200:
                data = response.json()
                return data.get("latitude"), data.get("longitude")
            else:
                st.error("Error al obtener datos de la API.")
        except requests.exceptions.RequestException as e:
            st.error(f"Error de conexión: {e}")
        return None, None

    # Visualización en Streamlit
    st.title("Aplicación de Ubicación GPS en Tiempo Real")

    # Obtener y mostrar los datos de la ubicación
    latitude, longitude = obtener_datos_gps()

    if latitude and longitude:
        st.write(f"Latitud: {latitude}")
        st.write(f"Longitud: {longitude}")

        # Crear un mapa centrado en las coordenadas actuales
        map_location = [latitude, longitude]
        map_obj = folium.Map(location=map_location, zoom_start=15)
        folium.Marker(map_location, tooltip="Ubicación Actual").add_to(map_obj)

        # Mostrar el mapa en Streamlit
        st_folium(map_obj, width=700, height=500)
    else:
        st.write("Esperando datos del receptor GPS...")