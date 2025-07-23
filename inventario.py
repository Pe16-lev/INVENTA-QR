import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)
import sqlite3

DB_NAME = 'inventario.db'

def crear_tabla():
    '''Crea la tabla de productos si no existe.'''
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            "Numero Serial" TEXT,
            "Tipo de equipo" TEXT,
            Marca TEXT,
            Modelo TEXT,
            Cantidad INTEGER NOT NULL,
            Fecha_adquisicion TEXT,
            Estado_actual TEXT,
            Garantia TEXT,
            Proveedor TEXT,
            Costo REAL,
            Responsable TEXT
        )
    ''')
    conn.commit()
    conn.close()

def agregar_producto(Numero_Serial, Tipo_de_equipo, Marca, Modelo, Cantidad, Fecha_adquisicion, Estado_actual, Garantia, Proveedor, Costo, Responsable):
    '''Agrega un producto al inventario.'''
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO productos (
            "Numero Serial", 
            "Tipo de equipo", 
            Marca, 
            Modelo, 
            Cantidad, 
            Fecha_adquisicion, 
            Estado_actual, 
            Garantia, 
            Proveedor, 
            Costo, 
            Responsable
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        Numero_Serial, 
        Tipo_de_equipo, 
        Marca, 
        Modelo, 
        Cantidad, 
        Fecha_adquisicion, 
        Estado_actual, 
        Garantia, 
        Proveedor, 
        Costo, 
        Responsable
    ))
    conn.commit()
    conn.close()


def buscar_producto_por_qr(codigo_qr):
    # Esta función ya no es válida porque la columna codigo_qr fue eliminada
    return None