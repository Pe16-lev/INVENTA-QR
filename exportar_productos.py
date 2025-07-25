import sqlite3
import json
import os

DB_NAME = 'inventario.db'
JSON_PATH = os.path.join('codigo', 'productos.json')  # Cambiado a 'telaraña'

campos = [
    "Numero Serial", "Tipo de equipo", "Marca", "Modelo", "Cantidad",
    "Fecha de adquisición", "Estado actual", "Garantía", "Proveedor", "Costo", "Responsable"
]

def exportar_productos():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT "Numero Serial", "Tipo de equipo", "Marca", "Modelo", "Cantidad", "Fecha de adquisición", "Estado actual", "Garantía", "Proveedor", "Costo", "Responsable" FROM productos')
    productos = cursor.fetchall()
    lista = []
    for prod in productos:
        item = {campo: valor for campo, valor in zip(campos, prod)}
        lista.append(item)
    conn.close()
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(lista, f, ensure_ascii=False, indent=2)
    print(f"Exportados {len(lista)} productos a {JSON_PATH}")

if __name__ == "__main__":
    exportar_productos()