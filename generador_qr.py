# generador_qr.py
# Funciones para generar códigos QR para productos del inventario

import qrcode
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1) 

def generar_qr(numero_serie, archivo_salida):
    url = f"https://pe16-lev.github.io/INVENTA-QR/?serial={numero_serie}"
    img = qrcode.make(url)
    # Agregar el número de serie como texto debajo del QR
    from PIL import Image, ImageDraw, ImageFont
    qr_width, qr_height = img.size
    # Intentar cargar una fuente, si no, usar la predeterminada
    try:
        font = ImageFont.truetype("arial.ttf", 28)
    except:
        font = ImageFont.load_default()
    text = str(numero_serie)
    # Medir el texto
    dummy_img = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(dummy_img)
    text_width, text_height = draw.textsize(text, font=font)
    # Crear nueva imagen con espacio extra para el texto
    new_height = qr_height + text_height + 16
    new_img = Image.new("RGB", (qr_width, new_height), "white")
    new_img.paste(img, (0, 0))
    draw = ImageDraw.Draw(new_img)
    # Centrar el texto debajo del QR
    text_x = (qr_width - text_width) // 2
    text_y = qr_height + 8
    draw.text((text_x, text_y), text, fill="black", font=font)
    new_img.save(archivo_salida)
    print(f"Código QR guardado en {archivo_salida} con URL: {url}")