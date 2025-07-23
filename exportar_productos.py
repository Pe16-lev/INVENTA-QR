import sqlite3
import json
import os

DB_NAME = 'inventario.db'
JSON_PATH = os.path.join('web', 'productos.json')

campos = [
    "Numero Serial", "Tipo de equipo", "Marca", "Modelo", "Cantidad",
    "Fecha_adquisicion", "Estado_actual", "Garantia", "Proveedor", "Costo", "Responsable"
]

def exportar_productos():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    lista = []
    for prod in productos:
        item = {
            "Numero_Serial": prod[0],
            "Tipo_de_equipo": prod[1],
            "Marca": prod[2],
            "Modelo": prod[3],
            "Cantidad": prod[4],
            "Fecha_adquisicion": prod[5],
            "Estado_actual": prod[6],
            "Garantia": prod[7],
            "Proveedor": prod[8],
            "Costo": prod[9],
            "Responsable": prod[10]
        }
        lista.append(item)
    conn.close()
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(lista, f, ensure_ascii=False, indent=2)
    print(f"Exportados {len(lista)} productos a {JSON_PATH}")

if __name__ == "__main__":
    exportar_productos()
