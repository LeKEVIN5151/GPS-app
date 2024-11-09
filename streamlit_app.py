import streamlit as st
import pynmea2
import folium
from streamlit_folium import st_folium
import serial
from flask import Flask, request, jsonify
from threading import Thread
import pandas as pd
from geopy.distance import geodesic
import plotly.express as px
import pydeck as pdk
import requests

# Inicializa la app Flask
app = Flask(__name__)

# Interfaz principal de Streamlit
def streamlit_ui():
    st.sidebar.title("Selecciona el servicio")
    opcion = st.sidebar.radio(
        "Servicios",
        ["Ubicación mediante trama NMEA", "Análisis Simulador de Vuelo", "Cálculo de área", "Ubicación Usuario", "Ubicación G-STAR IV"]
    )

    # Procesamiento NMEA
    if opcion == "Ubicación mediante trama NMEA":
        st.header("Ubicación mediante trama NMEA")
        nmea_input = st.text_input("Ingresa la trama NMEA")
        if nmea_input:
            try:
                msg = pynmea2.parse(nmea_input)
                lat, lon = msg.latitude, msg.longitude
                st.write(f"Latitud: {lat}")
                st.write(f"Longitud: {lon}")
                map_location = folium.Map(location=[lat, lon], zoom_start=15)
                folium.Marker([lat, lon], tooltip="Ubicación actual").add_to(map_location)
                st_folium(map_location, width=900, height=700)
            except Exception as e:
                st.error(f"Error procesando la trama NMEA: {e}")

    # Análisis de simulador de vuelo
    elif opcion == "Análisis Simulador de Vuelo":
        st.header("Análisis Simulador de Vuelo")
        archivo = st.file_uploader("Selecciona un archivo .txt", type="txt")
        if archivo:
            datos_vuelo = pd.read_csv(archivo, sep=';', skiprows=1,
                                      names=["Tiempo", "Lat", "Long", "AltMSL", "AltRad", "Roll", "Pitch", "Yaw"])
            # Cálculos de métricas
            tiempo_total = (pd.to_datetime(datos_vuelo['Tiempo'].iloc[-1]) - pd.to_datetime(datos_vuelo['Tiempo'].iloc[0])).total_seconds() / 60
            distancias = [geodesic((datos_vuelo['Lat'][i], datos_vuelo['Long'][i]), 
                                   (datos_vuelo['Lat'][i+1], datos_vuelo['Long'][i+1])).meters 
                          for i in range(len(datos_vuelo) - 1)]
            velocidad_horizontal = sum(distancias) / max(tiempo_total, 1)
            st.write(f"Tiempo total de vuelo (min): {tiempo_total:.2f}")
            st.write(f"Velocidad horizontal promedio (m/s): {velocidad_horizontal:.2f}")
            
            # Mapa de recorrido
            df = pd.DataFrame({'lat': datos_vuelo['Lat'], 'lon': datos_vuelo['Long']})
            st.map(df, size=0.001)

    # Datos GPS G-STAR IV
    elif opcion == "Ubicación G-STAR IV":
        st.header("Ubicación G-STAR IV")
        API_URL = "http://0.0.0.0:5000/location"
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

        lat, lon = obtener_datos_gps()
        if lat and lon:
            st.write(f"Latitud: {lat}")
            st.write(f"Longitud: {lon}")
            map_location = folium.Map(location=[lat, lon], zoom_start=15)
            folium.Marker([lat, lon], tooltip="Ubicación Actual").add_to(map_location)
            st_folium(map_location, width=700, height=500)

# Endpoint en Flask para recibir datos
@app.route('/location', methods=['POST'])
def recibir_datos():
    data = request.get_json()
    st.session_state.latitude = data.get("latitude", 0.0)
    st.session_state.longitude = data.get("longitude", 0.0)
    return jsonify({"status": "received"})

# Ejecutar Flask en un hilo
def run_flask():
    app.run(port=5000, debug=False, use_reloader=False)

if __name__ == "__main__":
    flask_thread = Thread(target=run_flask)
    flask_thread.start()
    streamlit_ui()
