import streamlit as st
import pynmea2
import folium
from streamlit_folium import st_folium

# Título principal de la aplicación
st.title("Aplicación de Servicios")

# Menú lateral para elegir la sección
st.sidebar.title("Selecciona el servicio")
opcion = st.sidebar.radio("Servicios", ["Ubicación mediante trama NMEA", "Análisis Simulador de Vuelo", "Cálculo de área"])

# Sección "Ubicación mediante trama NMEA"
if opcion == "Ubicación mediante trama NMEA":
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
            st_folium(map_location, width=700, height=500)

        except Exception as e:
            st.error(f"Error procesando la trama NMEA: {e}")

# Sección "Análisis Simulador de Vuelo"
elif opcion == "Análisis Simulador de Vuelo":
    st.header("Análisis Simulador de Vuelo")
    st.write("Aquí puedes añadir el análisis del simulador de vuelo.")

# Sección "Cálculo de área"
elif opcion == "Cálculo de área":
    st.header("Cálculo de área")
    st.write("Aquí puedes añadir el cálculo de área.")