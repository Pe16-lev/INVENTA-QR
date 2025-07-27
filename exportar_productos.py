import sqlite3
import json
import os

# Nombre de la base de datos
DB_NAME = 'inventario.db'


# Ruta donde se guardará productos.json (ahora en la raíz)
ARCHIVO_JSON = 'productos.json'

import sqlite3
def obtener_campos_tabla():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('PRAGMA table_info(productos)')
    campos = [row[1] for row in cursor.fetchall()]
    conn.close()
    return campos


def exportar_productos():
    campos = obtener_campos_tabla()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    columnas_sql = ', '.join([f'"{c}"' for c in campos])
    cursor.execute(f'SELECT {columnas_sql} FROM productos')
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
