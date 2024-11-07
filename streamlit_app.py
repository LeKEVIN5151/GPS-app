import streamlit as st
import pynmea2
import folium
from streamlit_folium import st_folium

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
    st.header("Ubicación G-STAR IV")
    st.write("Visualización en tiempo real de la ubicación del GPS G-STAR IV")

    # Variables para almacenar las coordenadas en tiempo real
    if 'latitude' not in st.session_state:
        st.session_state.latitude = None
    if 'longitude' not in st.session_state:
        st.session_state.longitude = None

    # Función para leer datos desde el puerto serial
    def leer_datos_gps():
        try:
            ser = serial.Serial('/dev/ttyUSB0', 4800, timeout=1)  # Configura el puerto y la velocidad de baudios
            while True:
                line = ser.readline().decode('ascii', errors='replace')
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

    # Visualización en Streamlit
    st.title("Aplicación de Ubicación GPS en Tiempo Real")

    # Verifica si hay coordenadas disponibles
    if st.session_state.latitude and st.session_state.longitude:
        st.write(f"Latitud: {st.session_state.latitude}")
        st.write(f"Longitud: {st.session_state.longitude}")

        # Crear un mapa centrado en las coordenadas actuales
        map_location = [st.session_state.latitude, st.session_state.longitude]
        map_obj = folium.Map(location=map_location, zoom_start=15)
        folium.Marker(map_location, tooltip="Ubicación Actual").add_to(map_obj)

        # Mostrar el mapa en Streamlit
        st_folium(map_obj, width=700, height=500)
    else:
        st.write("Esperando datos del receptor GPS...")
