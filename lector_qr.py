# lector_qr.py
# Funciones para leer códigos QR usando la cámara o imágenes

import cv2
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)
from pyzbar import pyzbar

def leer_qr_desde_imagen(ruta_imagen):
    '''Lee y decodifica un código QR desde una imagen.'''
    imagen = cv2.imread(ruta_imagen)
    codigos = pyzbar.decode(imagen)
    for codigo in codigos:
        return codigo.data.decode('utf-8')
    return None