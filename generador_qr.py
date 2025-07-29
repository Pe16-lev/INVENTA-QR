# generador_qr.py
# Funciones para generar códigos QR para productos del inventario

import qrcode
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1) 

def generar_qr(numero_serie, archivo_salida):
    url = f"https://pe16-lev.github.io/INVENTA-QR/index.html?serial={numero_serie}"
    img = qrcode.make(url)
    img.save(archivo_salida)
    print(f"Código QR guardado en {archivo_salida} con URL: {url}")