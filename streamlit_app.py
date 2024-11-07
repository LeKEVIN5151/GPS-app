import streamlit as st
import pynmea2
import folium
from streamlit_folium import st_folium
import serial
from threading import Thread
import time
<<<<<<< HEAD
=======
import requests
>>>>>>> 96a7518 (version_1.0)

# Título principal de la aplicación
st.title("Aplicación de Servicios")

# Menú lateral para elegir la sección
st.sidebar.title("Selecciona el servicio")
opcion = st.sidebar.radio("Servicios", ["Ubicación mediante trama NMEA", "Análisis Simulador de Vuelo", "Cálculo de área", "Ubicación Usuario", "Ubicación G-STAR IV"])

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

# Sección "Ubicación Usuario"
elif opcion == "Ubicación Usuario":
    st.header("Ubicación Usuario")
    st.write("Aquí puedes añadir el análisis del simulador de vuelo.")

# Sección "Ubicación G-STAR IV"
elif opcion == "Ubicación G-STAR IV":
    API_URL = "http://localhost:5000/location"  # Cambia a tu dominio y puerto si necesario

    def obtener_datos_gps():
        try:
<<<<<<< HEAD
            ser = serial.Serial('/dev/ttyUSB0', 4800, timeout=1)  # Configura el puerto y la velocidad de baudios
            while True:
                line = ser.readline().decode('ascii', errors='replace')
                print(line)  # Mostrar cada línea en la terminal
                st.write(f"Trama recibida: {line}")  # Mostrar en la interfaz Streamlit

                if line.startswith("$GPGGA") or line.startswith("$GPRMC"):
                    try:
                        msg = pynmea2.parse(line)
                        if hasattr(msg, 'latitude') and hasattr(msg, 'longitude'):
                            st.session_state.latitude = msg.latitude
                            st.session_state.longitude = msg.longitude
                    except pynmea2.ParseError:
                        pass
                time.sleep(1)
        except serial.SerialException:
            st.error("Error de conexión con el dispositivo GPS. Verifique la conexión y el puerto.")

    # Inicia el hilo de lectura de GPS
    if 'gps_thread' not in st.session_state:
        st.session_state.gps_thread = Thread(target=leer_datos_gps, daemon=True)
        st.session_state.gps_thread.start()
=======
            response = requests.get(API_URL)
            if response.status_code == 200:
                data = response.json()
                return data.get("latitude"), data.get("longitude")
            else:
                st.error("Error al obtener datos de la API.")
        except requests.exceptions.RequestException as e:
            st.error(f"Error de conexión: {e}")
        return None, None
>>>>>>> 96a7518 (version_1.0)

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