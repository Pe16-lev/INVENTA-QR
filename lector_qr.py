# lector_qr.py
# Funciones para leer códigos QR usando la cámara o imágenes

import cv2
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)
from pyzbar import pyzbar

def leer_qr_desde_imagen(ruta_imagen):
    '''Lee y decodifica un código QR desde una imagen. Si el QR es una URL con ?serial=, extrae el número de serie.'''
    imagen = cv2.imread(ruta_imagen)
    codigos = pyzbar.decode(imagen)
    for codigo in codigos:
        data = codigo.data.decode('utf-8')
        # Si es una URL con ?serial=, extraer el número de serie
        if '?serial=' in data:
            import urllib.parse
            url = urllib.parse.urlparse(data)
            params = urllib.parse.parse_qs(url.query)
            serial = params.get('serial', [None])[0]
            return serial if serial else data
        return data
    return None