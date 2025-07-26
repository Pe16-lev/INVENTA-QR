import sqlite3
import json
import os

# Nombre de la base de datos
DB_NAME = 'inventario.db'

# Ruta donde se guardará productos.json
CARPETA_JSON = 'codigo'
ARCHIVO_JSON = os.path.join(CARPETA_JSON, 'productos.json')

# Asegurarse de que la carpeta 'codigo' existe
if not os.path.exists(CARPETA_JSON):
    os.makedirs(CARPETA_JSON)

# Campos que exportaremos (los que el HTML espera)
campos = [
    "Numero Serial", "Tipo de equipo", "Marca", "Modelo", "Cantidad",
    "Fecha de adquisición", "Estado actual", "Garantía", "Proveedor", "Costo", "Responsable"
]

def exportar_productos():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT "Numero Serial", "Tipo de equipo", "Marca", "Modelo", "Cantidad",
               "Fecha de adquisición", "Estado actual", "Garantía", "Proveedor", "Costo", "Responsable"
        FROM productos
    ''')
    
    productos = cursor.fetchall()
    lista = []

    for prod in productos:
        item = {campo: valor for campo, valor in zip(campos, prod)}
        lista.append(item)

    conn.close()

    with open(ARCHIVO_JSON, 'w', encoding='utf-8') as f:
        json.dump(lista, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Exportados {len(lista)} productos a {ARCHIVO_JSON}")

if __name__ == "__main__":
    exportar_productos()
