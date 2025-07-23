# generador_qr.py
# Funciones para generar códigos QR para productos del inventario

import qrcode
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1) 

def generar_qr(datos, archivo_salida):
    '''Genera un código QR con los datos proporcionados y lo guarda como imagen.'''
    img = qrcode.make(datos)
    img.save(archivo_salida)
    print(f"Código QR guardado en {archivo_salida}")