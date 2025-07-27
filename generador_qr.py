# generador_qr.py
# Funciones para generar códigos QR para productos del inventario

import qrcode
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1) 

def generar_qr(numero_serie, archivo_salida):
    url = f"https://pe16-lev.github.io/INVENTA-QR/?serial={numero_serie}"
    img = qrcode.make(url)
    from PIL import Image, ImageDraw, ImageFont
    qr_width, qr_height = img.size
    text = str(numero_serie)
    # Intentar cargar una fuente grande, si no, usar la predeterminada pero con escalado
    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except:
        font = ImageFont.load_default()
    # Medir el texto
    dummy_img = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(dummy_img)
    text_width, text_height = draw.textsize(text, font=font)
    # Si la fuente es muy pequeña, forzar un área más grande para el texto
    min_text_height = max(40, text_height)
    padding = 20
    new_height = qr_height + min_text_height + padding
    new_img = Image.new("RGB", (qr_width, new_height), "white")
    new_img.paste(img, (0, 0))
    draw = ImageDraw.Draw(new_img)
    # Centrar el texto debajo del QR
    text_x = (qr_width - text_width) // 2
    text_y = qr_height + (padding // 2)
    draw.text((text_x, text_y), text, fill="black", font=font)
    new_img.save(archivo_salida)
    print(f"Código QR guardado en {archivo_salida} con URL: {url}")