# Pasos para ejecutar el cliente gps.py
1. Mover los tres archivos `gps.py` y `requeriments.txt` a un directorio fuera de la carpeta de Github.
2. En ese directorio en el cual estan los dos archivos movidos generar un entorno virtual con el siguiente comando:
```bash
python3 -m venv .
```
3. Activamos el entorno virtual
```bash
source ./bin/activate
```
4. Instalamos las librerias necesarias:
```bash
pip install -r requeriments.txt
```
5. Damos permiso de ejecución al puerto donde esta conectado el GPS.
```bash
sudo chmod 666 /dev/ttyUSB0
```
6. Ejecutamos el archivo
```bash
python3 gps.py
```

## Aclaraciones
Para descativar el entorno virtual se debe realizar:
```bash
deactivate
```

Cada vez que se inicie el entorno virtual nuevamente deben darle permiso al puerto ttyUSB0.

*¡IMPORTANTE! si hay error con libreria serial desinstalar con `pip uninstall pyserial` y volver a instalar manualmente `pip install pyserial`*