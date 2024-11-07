import serial
import pynmea2
from flask import Flask, jsonify
import time
from threading import Thread
import pyserial

app = Flask(__name__)

# Variable para almacenar datos GPS
gps_data = {"latitude": None, "longitude": None}

def leer_datos_gps():
    try:
        print("Intentando abrir el puerto serial...")
        ser = serial.Serial('/dev/ttyUSB0', 4800, timeout=1)
        print("Puerto serial abierto correctamente.")
        
        while True:
            line = ser.readline().decode('ascii', errors='replace')
            print(f"Trama recibida: {line}")  # Muestra cada línea leída

            if line.startswith("$GPGGA") or line.startswith("$GPRMC"):
                try:
                    msg = pynmea2.parse(line)
                    if hasattr(msg, 'latitude') and hasattr(msg, 'longitude'):
                        gps_data["latitude"] = msg.latitude
                        gps_data["longitude"] = msg.longitude
                        print(f"Latitud: {gps_data['latitude']}, Longitud: {gps_data['longitude']}")  # Imprime coordenadas

                except pynmea2.ParseError:
                    print("Error al parsear la trama NMEA.")
                    
    except serial.SerialException as e:
        print(f"Error de conexión con el dispositivo GPS: {e}")

# Endpoint para obtener la ubicación actual
@app.route('/location', methods=['GET'])
def get_location():
    return jsonify(gps_data)

if __name__ == '__main__':
    # Inicia la lectura en otro hilo
    gps_thread = Thread(target=leer_datos_gps, daemon=True)
    gps_thread.start()
    
    app.run(host="0.0.0.0", port=5000)