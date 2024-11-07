import streamlit as st
import pynmea2
import folium

st.title("Aplicación de Ubicación GPS")

# Entrada de la trama NMEA
nmea_input = st.text_input("Ingrese la trama NMEA")

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
        folium.Marker([latitude, longitude]).add_to(map_location)
        st.components.v1.html(map_location._repr_html_(), width=700, height=500)

    except pynmea2.ParseError:
        st.error("Trama NMEA no válida. Intente nuevamente.")
