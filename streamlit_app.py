import streamlit as st
import pynmea2
import folium
from streamlit_folium import st_folium
import requests
from flask import Flask, request, jsonify
from threading import Thread

app = Flask(__name__)

# Variable global para almacenar las coordenadas GPS
gps_data = {"latitude": None, "longitude": None}

# Función para recibir datos GPS desde el cliente
@app.route('/receive_gps', methods=['POST'])
def receive_gps():
    global gps_data
    data = request.json
    gps_data["latitude"] = data.get("latitude")
    gps_data["longitude"] = data.get("longitude")
    return jsonify({"message": "Datos recibidos correctamente"}), 200

# Interfaz de Streamlit para mostrar la ubicación
def streamlit_ui():
    st.sidebar.title("Selecciona el servicio")
    opcion = st.sidebar.radio(
        "Servicios",
        ["Ubicación mediante trama NMEA", "Análisis Simulador de Vuelo", "Cálculo de área", "Ubicación Usuario", "Ubicación G-STAR IV"]
    )

    # Mostrar la ubicación recibida por el cliente
    if opcion == "Ubicación Usuario":
        st.header("Ubicación Usuario")
        if gps_data["latitude"] and gps_data["longitude"]:
            lat, lon = gps_data["latitude"], gps_data["longitude"]
            st.write(f"Latitud: {lat}")
            st.write(f"Longitud: {lon}")
            map_location = folium.Map(location=[lat, lon], zoom_start=15)
            folium.Marker([lat, lon], tooltip="Ubicación actual").add_to(map_location)
            st_folium(map_location, width=900, height=700)
        else:
            st.write("Esperando datos del GPS...")

# Función para ejecutar Flask en un hilo separado
def run_flask():
    app.run(host="0.0.0.0", port=5555)

# Inicia Flask en un hilo
flask_thread = Thread(target=run_flask, daemon=True)
flask_thread.start()

# Ejecuta Streamlit
if __name__ == "__main__":
    streamlit_ui()
