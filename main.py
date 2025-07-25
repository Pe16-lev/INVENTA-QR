import tkinter as tk
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)
from tkinter import messagebox, filedialog
from tkinter import ttk
from tkinter import PhotoImage
import os
from generador_qr import generar_qr
from lector_qr import leer_qr_desde_imagen
from inventario import crear_tabla, agregar_producto, buscar_producto_por_qr
from PIL import Image, ImageTk
from login import mostrar_login
from tkcalendar import DateEntry

def iniciar_ventana_inventario():
    root = tk.Tk()
    root.title("INVENTARIO CON CODIGOD QR")
    root.state('zoomed')
    dir_actual = os.path.dirname(os.path.abspath(__file__))

    # Fondo
    ruta_fondo = os.path.join(dir_actual, 'fondo_inventario.png')
    if os.path.exists(ruta_fondo):
        fondo_img = Image.open(ruta_fondo)
        fondo_img = fondo_img.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
        fondo_tk = ImageTk.PhotoImage(fondo_img)
        label_fondo = tk.Label(root, image=fondo_tk)
        label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
        label_fondo.image = fondo_tk

    # Menú
    def mostrar_ayuda():
        messagebox.showinfo("Ayuda", "Esta es la sección de ayuda.")

    def mostrar_acerca_de():
        messagebox.showinfo("Acerca de", "Inventario con Código QR\nVersión 1.0")

    # Eliminar menú superior y pasar opciones al menú lateral hamburguesa

    # --- Frame para botones superiores ---
    frame_botones_superior = tk.Frame(root, bg='white')
    frame_botones_superior.pack(fill="x", padx=10, pady=2)

    # --- Menú hamburguesa y panel lateral ---
    def toggle_menu_lateral():
        if menu_lateral.winfo_ismapped():
            menu_lateral.place_forget()
        else:
            menu_lateral.place(relx=1.0, rely=0, anchor='ne', relheight=1.0, width=260)

    # Botón hamburguesa (tres líneas)
    btn_hamburguesa = tk.Button(
        frame_botones_superior,
        text='≡',
        font=("Arial", 24, "bold"),
        bg='white',
        activebackground='#e0e0e0',
        bd=0,
        command=toggle_menu_lateral
    )
    btn_hamburguesa.pack(side="right", padx=(10, 0), pady=2)

    # Panel lateral oculto por defecto
    menu_lateral = tk.Frame(root, bg="#f5f5f5", bd=2, relief="ridge")
    # Opciones del menú lateral (solo las solicitadas)
    tk.Label(menu_lateral, text="Menú", font=("Arial", 16, "bold"), bg="#f5f5f5").pack(pady=(20, 10))

    # Solo botones principales
    tk.Button(menu_lateral, text="Salir", font=("Arial", 12), bg="#e0e0e0", command=root.destroy).pack(fill="x", padx=20, pady=5)

    def cambiar_cuenta():
        root.destroy()
        # Volver a mostrar login
        root_login = tk.Tk()
        root_login.withdraw()
        def on_login_exitoso():
            root_login.destroy()
            iniciar_ventana_inventario()
        mostrar_login(root_login, on_login_exitoso)
        root_login.mainloop()

    tk.Button(menu_lateral, text="Cambiar cuenta", font=("Arial", 12), bg="#e0e0e0", command=cambiar_cuenta).pack(fill="x", padx=20, pady=5)
    def mostrar_perfil():
        # Obtener usuario y correo reales del usuario logueado
        import sqlite3
        usuario_activo = getattr(root, 'usuario_activo', None)
        if usuario_activo is None:
            messagebox.showerror("Error", "No se pudo obtener el usuario activo.")
            return
        try:
            conn = sqlite3.connect('inventario.db')
            cursor = conn.cursor()
            cursor.execute('SELECT usuario, email FROM usuarios WHERE usuario = ?', (usuario_activo,))
            row = cursor.fetchone()
            if row:
                nombre_usuario, correo_usuario = row
            else:
                nombre_usuario, correo_usuario = usuario_activo, ''
            conn.close()
        except Exception as e:
            messagebox.showerror("Error de base de datos", f"No se pudo obtener el usuario: {e}")
            return

        usuario = {
            'nombre': nombre_usuario,
            'correo': correo_usuario,
            'cargo': 'Administrador',  # Puedes personalizar si tienes este dato en BD
            'telefono': '999-999-9999' # Puedes personalizar si tienes este dato en BD
        }

        ventana_perfil = tk.Toplevel(root)
        ventana_perfil.title("Perfil de usuario")
        ventana_perfil.geometry("400x520")
        ventana_perfil.configure(bg="#f5f5f5")
        ventana_perfil.grab_set()

        tk.Label(ventana_perfil, text="Perfil de usuario", font=("Arial", 16, "bold"), bg="#f5f5f5").pack(pady=(20, 10))

        # Nombre de usuario y correo (no editables)
        tk.Label(ventana_perfil, text=f"Nombre de usuario: {usuario['nombre']}", font=("Arial", 12), bg="#f5f5f5").pack(pady=5)
        tk.Label(ventana_perfil, text=f"Correo electrónico: {usuario['correo']}", font=("Arial", 12), bg="#f5f5f5").pack(pady=5)

        # Campos editables
        frame_edit = tk.Frame(ventana_perfil, bg="#f5f5f5")
        frame_edit.pack(pady=5)
        tk.Label(frame_edit, text="Cargo:", font=("Arial", 12), bg="#f5f5f5").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        entry_cargo = tk.Entry(frame_edit, font=("Arial", 12), width=22)
        entry_cargo.insert(0, usuario['cargo'])
        entry_cargo.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(frame_edit, text="Número de teléfono:", font=("Arial", 12), bg="#f5f5f5").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        entry_telefono = tk.Entry(frame_edit, font=("Arial", 12), width=22)
        entry_telefono.insert(0, usuario['telefono'])
        entry_telefono.grid(row=1, column=1, padx=5, pady=5)

        def guardar_edicion_perfil():
            nuevo_cargo = entry_cargo.get().strip()
            nuevo_tel = entry_telefono.get().strip()
            if not nuevo_cargo or not nuevo_tel:
                messagebox.showwarning("Campos vacíos", "Completa ambos campos.", parent=ventana_perfil)
                return
            usuario['cargo'] = nuevo_cargo
            usuario['telefono'] = nuevo_tel
            messagebox.showinfo("Guardado", "Datos actualizados (solo en memoria, personaliza para guardar en BD)", parent=ventana_perfil)

        tk.Button(ventana_perfil, text="Guardar cambios", font=("Arial", 12), bg="#4CAF50", fg="white", command=guardar_edicion_perfil).pack(pady=10)

        # --- Cambio de contraseña en la misma ventana ---
        frame_pass = tk.LabelFrame(ventana_perfil, text="Cambiar contraseña", font=("Arial", 12, "bold"), bg="#f5f5f5", fg="#2980b9", bd=2, relief="groove")
        frame_pass.pack(pady=15, padx=20, fill="x")
        tk.Label(frame_pass, text="Nueva contraseña:", font=("Arial", 11), bg="#f5f5f5").pack(pady=(10, 2))
        entry_nueva = tk.Entry(frame_pass, show="*", font=("Arial", 11))
        entry_nueva.pack(pady=2)
        tk.Label(frame_pass, text="Confirmar contraseña:", font=("Arial", 11), bg="#f5f5f5").pack(pady=2)
        entry_confirmar = tk.Entry(frame_pass, show="*", font=("Arial", 11))
        entry_confirmar.pack(pady=2)

        def guardar_nueva():
            nueva = entry_nueva.get()
            confirmar = entry_confirmar.get()
            if not nueva or not confirmar:
                messagebox.showwarning("Campos vacíos", "Completa ambos campos.", parent=ventana_perfil)
                return
            if nueva != confirmar:
                messagebox.showerror("Error", "Las contraseñas no coinciden.", parent=ventana_perfil)
                return
            # Guardar la nueva contraseña en la base de datos
            import sqlite3
            try:
                conn = sqlite3.connect('inventario.db')
                cursor = conn.cursor()
                # Usar el campo usuario como identificador
                cursor.execute('UPDATE usuarios SET contrasena = ? WHERE usuario = ?', (nueva, usuario['nombre']))
                if cursor.rowcount == 0:
                    messagebox.showerror("Error", "No se encontró el usuario para actualizar la contraseña.", parent=ventana_perfil)
                else:
                    conn.commit()
                    messagebox.showinfo("Éxito", "Contraseña cambiada correctamente.", parent=ventana_perfil)
                    entry_nueva.delete(0, tk.END)
                    entry_confirmar.delete(0, tk.END)
                conn.close()
            except Exception as e:
                messagebox.showerror("Error de base de datos", f"No se pudo actualizar la contraseña:\n{e}", parent=ventana_perfil)

        tk.Button(frame_pass, text="Guardar contraseña", font=("Arial", 11, "bold"), bg="#2980b9", fg="white", command=guardar_nueva).pack(pady=10)

        tk.Button(ventana_perfil, text="Cerrar", font=("Arial", 12), bg="#e0e0e0", command=ventana_perfil.destroy).pack(pady=10)

    tk.Button(menu_lateral, text="Cerrar menú", font=("Arial", 12), bg="#e0e0e0", command=toggle_menu_lateral).pack(fill="x", padx=20, pady=5)

    # Iconos
    def cargar_icono(ruta, size):
        if os.path.exists(ruta):
            img = Image.open(ruta).resize(size, Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        return None

    icono_agregar_path = os.path.join(dir_actual, 'icono_agregar.png')
    icono_buscar_path = os.path.join(dir_actual, 'icono_QR.png')
    icono_generar_qr_path = os.path.join(dir_actual, 'icono_QR.png')
    # Cargar iconos y mantener referencia en el objeto root para evitar que desaparezcan
    root.icono_agregar = cargar_icono(icono_agregar_path, (48, 48))
    root.icono_buscar = cargar_icono(icono_buscar_path, (48, 48))
    root.icono_generar_qr = cargar_icono(icono_generar_qr_path, (48, 48))
    icono_refresh_path = os.path.join(dir_actual, 'icono_refresh.png')
    root.icono_refresh = cargar_icono(icono_refresh_path, (48, 48))

    def refrescar_tabla():
        mostrar_productos()
        messagebox.showinfo("Refrescado", "La tabla se ha actualizado.")

    btn_refresh = tk.Button(
        frame_botones_superior,
        text="Refrescar",
        command=refrescar_tabla,
        image=root.icono_refresh,
        compound="left" if root.icono_refresh else None,
        width=160,
        height=40,
        padx=2,
        pady=2,
        bg='white',
        activebackground='white',
        font=("Arial", 11, "bold")
    )
    btn_refresh.pack(side="left", padx=5)

    def mostrar_productos():
        for row in tabla.get_children():
            tabla.delete(row)
        import sqlite3
        try:
            conn = sqlite3.connect('inventario.db')
            cursor = conn.cursor()
            cursor.execute('SELECT "Numero Serial", "Tipo de equipo", "Marca", "Modelo", "Cantidad", "Fecha_adquisicion", "Estado_actual", "Garantia", "Proveedor", "Costo", "Responsable" FROM productos')
            productos = cursor.fetchall()
            print('DEBUG productos desde la base de datos:', productos)
            for prod in productos:
                tabla.insert('', 'end', values=prod)
            conn.close()
        except Exception as e:
            print('ERROR al mostrar productos:', e)
            messagebox.showerror('Error de base de datos', f'Ocurrió un error al consultar la base de datos:\n{e}')

    def abrir_ventana_agregar():
        ventana_agregar = tk.Toplevel()
        ventana_agregar.title("Agregar Producto")
        ventana_agregar.state('zoomed')
        ventana_agregar.configure(bg="#8CA89C")
        ventana_agregar.grab_set()

        frame_formulario = tk.Frame(ventana_agregar, bg="white", bd=2, relief="groove")
        frame_formulario.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)

        campos = [
            "Número de serie", "Tipo de equipo", "Marca", "Modelo", "Cantidad",
            "Fecha de adquisición", "Estado actual", "Garantía",
            "Proveedor", "Costo", "Responsable"
        ]
        entradas = {}
        iconos = {
            "Número de serie": "🔢",
            "Tipo de equipo": "🖥️",
            "Marca": "🏷️",
            "Modelo": "📦",
            "Cantidad": "🔢",
            "Fecha de adquisición": "📅",
            "Estado actual": "📊",
            "Garantía": "📃",
            "Proveedor": "🏭",
            "Costo": "💰",
            "Responsable": "👤"
        }
        for i, campo in enumerate(campos):
            col = 0 if i < 6 else 2
            row = i if i < 6 else i - 6
            emoji = iconos.get(campo, "")
            label = tk.Label(frame_formulario, text=f"{emoji} {campo}:", bg="white", anchor="w", font=("Arial", 12))
            label.grid(row=row, column=col, sticky="e", padx=20, pady=10)
            if campo == "Fecha de adquisición":
                entrada = DateEntry(frame_formulario, date_pattern='yyyy-mm-dd', width=25)
                entrada.grid(row=row, column=col+1, sticky="w", padx=10, pady=10)
                entradas[campo] = entrada
            elif campo == "Estado actual":
                entrada = ttk.Combobox(frame_formulario, values=["Nuevo", "Usado", "Dañado", "Baja"], state="readonly", width=28, font=("Arial", 11))
                entrada.set("Nuevo")
                entrada.grid(row=row, column=col+1, sticky="w", padx=10, pady=10)
                entradas[campo] = entrada
            elif campo == "Garantía":
                frame_garantia = tk.Frame(frame_formulario, bg="white")
                cb_anos = ttk.Combobox(frame_garantia, values=[str(j) for j in range(0, 11)], width=4, state="readonly")
                cb_anos.set("0")
                tk.Label(frame_garantia, text="Años", bg="white").pack(side="left")
                cb_anos.pack(side="left")
                cb_meses = ttk.Combobox(frame_garantia, values=[str(j) for j in range(0, 13)], width=4, state="readonly")
                cb_meses.set("0")
                tk.Label(frame_garantia, text="Meses", bg="white").pack(side="left")
                cb_meses.pack(side="left")
                cb_dias = ttk.Combobox(frame_garantia, values=[str(j) for j in range(0, 32)], width=4, state="readonly")
                cb_dias.set("0")
                tk.Label(frame_garantia, text="Días", bg="white").pack(side="left")
                cb_dias.pack(side="left")
                frame_garantia.grid(row=row, column=col+1, sticky="w", padx=10, pady=10)
                entradas[campo] = (cb_anos, cb_meses, cb_dias)
            else:
                entrada = tk.Entry(frame_formulario, width=30, font=("Arial", 11))
                entrada.grid(row=row, column=col+1, sticky="w", padx=10, pady=10)
                entradas[campo] = entrada
        def guardar_producto():
            import subprocess
            datos = []
            for c in campos:
                if c == "Garantía":
                    cb_anos, cb_meses, cb_dias = entradas[c]
                    valor = f"{cb_anos.get()} años, {cb_meses.get()} meses, {cb_dias.get()} días"
                    datos.append(valor)
                else:
                    datos.append(entradas[c].get().strip())
            if not all(datos):
                messagebox.showwarning("Campos incompletos", "Por favor completa todos los campos.")
                return
            try:
                agregar_producto(*datos)
                # Exportar productos automáticamente
                subprocess.run(["python", "exportar_productos.py"], check=True)
                # Hacer commit y push automático
                subprocess.run(["git", "add", "telaraña/productos.json"], check=True)
                subprocess.run(["git", "commit", "-m", "Actualización automática de productos.json"], check=True)
                subprocess.run(["git", "push"], check=True)
                messagebox.showinfo("Éxito", "Producto agregado y datos web actualizados.")
                ventana_agregar.destroy()
                mostrar_productos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el producto ni actualizar la web:\n{e}")
        total_filas = max(6, len(campos) - 6)
        btn_guardar = tk.Button(
            frame_formulario,
            text="💾 Guardar producto",
            command=guardar_producto,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10
        )
        btn_guardar.grid(row=total_filas + 1, column=0, columnspan=4, pady=30)

    btn_ventana_agregar = tk.Button(
        frame_botones_superior,
        text="Agregar producto",
        command=abrir_ventana_agregar,
        image=root.icono_agregar,
        compound="left" if root.icono_agregar else None,
        width=160,
        height=40,
        padx=2,
        pady=2,
        bg='white',
        activebackground='white'
    )
    def generar_qr_seleccion():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Selecciona un producto", "Debes seleccionar un producto de la tabla.")
            return
        item = tabla.item(seleccion[0])
        valores = item['values']
        numero_serial = valores[0]
        modelo = valores[3]
        # Cambiar el QR para que sea una URL con el número de serie
        url_base = "https://Pe16-lev.github.io/INVENTA-QR/web/producto.html?serial="
        datos_qr = f"{url_base}{numero_serial}"
        print(f"DEBUG QR: {datos_qr}")  # Depuración: muestra la URL que se codificará en el QR
        # Preguntar al usuario dónde guardar el QR
        from tkinter import filedialog
        qr_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("Imagen PNG", "*.png")],
            initialfile=f"{numero_serial}_qr.png",
            title="Guardar código QR como..."
        )
        if not qr_path:
            return  # El usuario canceló
        generar_qr(datos_qr, qr_path)
        # Ya no se muestra la ventana con la imagen del QR
        messagebox.showinfo("Éxito", f"QR generado y guardado en {qr_path}")

    # --- Frame tabla con título ---
    frame_tabla_con_titulo = tk.Frame(root, bg='white')
    frame_tabla_con_titulo.place(relx=0.5, rely=0.55, anchor='center', width=1400, height=650)

    label_titulo_tabla = tk.Label(frame_tabla_con_titulo, text="TABLA DE PRODUCTOS", font=("Arial", 20, "bold"), fg="#000000", bg='white')
    label_titulo_tabla.pack(pady=(0, 10))

    frame_tabla = tk.LabelFrame(frame_tabla_con_titulo, text="", bg='white', bd=2, relief="groove")
    frame_tabla.pack(fill="both", expand=True)

    # Crear la tabla dentro del frame_tabla
    columnas = [
        "Número de serie", "Tipo de equipo", "Marca", "Modelo", "Cantidad",
        "Fecha de adquisición", "Estado actual", "Garantía", "Proveedor", "Costo", "Responsable"
    ]
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=12)
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=120, anchor="center")

    # Scrollbar vertical para la tabla
    scrollbar_y = tk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=scrollbar_y.set)
    scrollbar_y.pack(side="right", fill="y")

    tabla.pack(fill="both", expand=True, padx=10, pady=10)

    # Eliminar función duplicada, ya existe la versión correcta más arriba

    def abrir_ventana_agregar():
        ventana_agregar = tk.Toplevel()
        ventana_agregar.title("Agregar Producto")
        ventana_agregar.state('zoomed')
        ventana_agregar.configure(bg="#8CA89C")
        ventana_agregar.grab_set()
        # ...

        frame_formulario = tk.Frame(ventana_agregar, bg="white", bd=2, relief="groove")
        frame_formulario.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)

        campos = [
            "Número de serie", "Tipo de equipo", "Marca", "Modelo", "Cantidad",
            "Fecha de adquisición", "Estado actual", "Garantía",
            "Proveedor", "Costo", "Responsable"
        ]
        entradas = {}

        iconos = {
            "Número de serie": "🔢",
            "Tipo de equipo": "🖥️",
            "Marca": "🏷️",
            "Modelo": "📦",
            "Cantidad": "🔢",
            "Fecha de adquisición": "📅",
            "Estado actual": "📊",
            "Garantía": "📃",
            "Proveedor": "🏭",
            "Costo": "💰",
            "Responsable": "👤"
        }

        for i, campo in enumerate(campos):
            col = 0 if i < 6 else 2
            row = i if i < 6 else i - 6
            emoji = iconos.get(campo, "")
            label = tk.Label(frame_formulario, text=f"{emoji} {campo}:", bg="white", anchor="w", font=("Arial", 12))
            label.grid(row=row, column=col, sticky="e", padx=20, pady=10)

            if campo == "Fecha de adquisición":
                entrada = DateEntry(frame_formulario, date_pattern='yyyy-mm-dd', width=25)
            elif campo == "Estado actual":
                entrada = ttk.Combobox(frame_formulario, values=["Nuevo", "Usado", "Dañado", "Baja"], state="readonly", width=28, font=("Arial", 11))
                entrada.set("Nuevo")
            else:
                entrada = tk.Entry(frame_formulario, width=30, font=("Arial", 11))
            entrada.grid(row=row, column=col+1, sticky="w", padx=10, pady=10)
            entradas[campo] = entrada

        def guardar_producto():
            datos = [entradas[c].get().strip() for c in campos]
            if not all(datos):
                messagebox.showwarning("Campos incompletos", "Por favor completa todos los campos.")
                return
            # Ya no se fuerza a número, se permite cualquier texto en Cantidad y Costo
            try:
                agregar_producto(*datos)
                messagebox.showinfo("Éxito", "Producto agregado correctamente.")
                ventana_agregar.destroy()
                mostrar_productos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el producto:\n{e}")

        total_filas = max(6, len(campos) - 6)
        btn_guardar = tk.Button(
            frame_formulario,
            text="💾 Guardar producto",
            command=guardar_producto,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10
        )
        btn_guardar.grid(row=total_filas + 1, column=0, columnspan=4, pady=30)

    btn_ventana_agregar = tk.Button(
        frame_botones_superior,
        text="Agregar producto",
        command=abrir_ventana_agregar,
        image=root.icono_agregar,
        compound="left" if root.icono_agregar else None,
        width=160,
        height=40,
        padx=2,
        pady=2,
        bg='white',
        activebackground='white'
    )
    btn_ventana_agregar.pack(side="left", padx=5)
    def buscar_producto_gui():
        file_path = filedialog.askopenfilename(
            title="Selecciona una imagen QR",
            filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg;*.bmp")]
        )
        if not file_path:
            return
        qr_data = leer_qr_desde_imagen(file_path)
        if not qr_data:
            messagebox.showerror("Error", "No se pudo leer el código QR de la imagen seleccionada.")
            return
        producto = buscar_producto_por_qr(qr_data)
        if producto:
            for row in tabla.get_children():
                if str(tabla.item(row)['values'][0]) == str(producto[0]):
                    tabla.selection_set(row)
                    tabla.see(row)
                    break
            messagebox.showinfo("Producto encontrado", f"Producto encontrado:\n{producto}")
        else:
            messagebox.showwarning("No encontrado", "No se encontró ningún producto con ese QR.")

    btn_buscar_top = tk.Button(
        frame_botones_superior,
        text="Buscar por QR",
        command=buscar_producto_gui,
        image=root.icono_buscar,
        compound="left" if root.icono_buscar else None,
        width=160,
        height=40,
        padx=2,
        pady=2,
        bg='white',
        activebackground='white'
    )
    btn_buscar_top.pack(side="left", padx=5)

    def generar_qr_seleccion():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Selecciona un producto", "Debes seleccionar un producto de la tabla.")
            return
        item = tabla.item(seleccion[0])
        valores = item['values']
        numero_serial = valores[0]
        modelo = valores[3]
        # Cambiar el QR para que sea una URL con el número de serie
        url_base = "https://Pe16-lev.github.io/INVENTA-QR/telaraña/producto.html?serial="
        datos_qr = f"{url_base}{numero_serial}"
        # Preguntar al usuario dónde guardar el QR
        from tkinter import filedialog
        qr_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("Imagen PNG", "*.png")],
            initialfile=f"{numero_serial}_qr.png",
            title="Guardar código QR como..."
        )
        if not qr_path:
            return  # El usuario canceló
        generar_qr(datos_qr, qr_path)
        # Ya no se muestra la ventana con la imagen del QR
        messagebox.showinfo("Éxito", f"QR generado y guardado en {qr_path}")

    btn_generar_qr = tk.Button(
        frame_botones_superior,
        text="Generar QR",
        command=generar_qr_seleccion,
        image=root.icono_generar_qr,
        compound="left" if root.icono_generar_qr else None,
        width=160,
        height=40,
        padx=2,
        pady=2,
        bg='white',
        activebackground='white'
    )
    btn_generar_qr.pack(side="left", padx=5)

    # --- Frame tabla con título ---
    frame_tabla_con_titulo = tk.Frame(root, bg='white')
    frame_tabla_con_titulo.place(relx=0.5, rely=0.55, anchor='center', width=1400, height=650)

    label_titulo_tabla = tk.Label(frame_tabla_con_titulo, text="TABLA DE PRODUCTOS", font=("Arial", 20, "bold"), fg="#000000", bg='white')
    label_titulo_tabla.pack(pady=(0, 10))

    frame_tabla = tk.LabelFrame(frame_tabla_con_titulo, text="", bg='white', bd=2, relief="groove")
    frame_tabla.pack(fill="both", expand=True)

    # Crear la tabla dentro del frame_tabla
    columnas = [
        "Número de serie", "Tipo de equipo", "Marca", "Modelo", "Cantidad",
        "Fecha de adquisición", "Estado actual", "Garantía", "Proveedor", "Costo", "Responsable"
    ]
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=12)
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=120, anchor="center")

    # Scrollbar vertical para la tabla
    scrollbar_y = tk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=scrollbar_y.set)
    scrollbar_y.pack(side="right", fill="y")

    tabla.pack(fill="both", expand=True, padx=10, pady=10)

    # --- Botones de acción para editar y eliminar ---
    frame_acciones = tk.Frame(frame_tabla, bg='white')
    frame_acciones.pack(fill="x", padx=10, pady=5)

    def eliminar_producto():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Selecciona un producto", "Debes seleccionar un producto de la tabla.")
            return
        item = tabla.item(seleccion[0])
        valores = item['values']
        numero_serial = valores[0]
        if messagebox.askyesno("Confirmar", f"¿Seguro que deseas eliminar el producto con Número Serial {numero_serial}?"):
            import sqlite3
            conn = sqlite3.connect('inventario.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM productos WHERE "Numero Serial" = ?', (numero_serial,))
            conn.commit()
            conn.close()
            mostrar_productos()
            messagebox.showinfo("Eliminado", "Producto eliminado correctamente.")

    def editar_producto():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Selecciona un producto", "Debes seleccionar un producto de la tabla.")
            return
        item = tabla.item(seleccion[0])
        valores = item['values']
        ventana_editar = tk.Toplevel()
        ventana_editar.title("Editar Producto")
        ventana_editar.state('zoomed')
        ventana_editar.configure(bg="#f0f0f0")
        ventana_editar.grab_set()
        frame_formulario = tk.Frame(ventana_editar, bg="white", bd=2, relief="groove")
        frame_formulario.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)
        campos = [
            "Número de serie", "Tipo de equipo", "Marca", "Modelo", "Cantidad",
            "Fecha de adquisición", "Estado actual", "Garantía",
            "Proveedor", "Costo", "Responsable"
        ]
        entradas = {}
        iconos = {
            "Número de serie": "🔢",
            "Tipo de equipo": "🖥️",
            "Marca": "🏷️",
            "Modelo": "📦",
            "Cantidad": "🔢",
            "Fecha de adquisición": "📅",
            "Estado actual": "📊",
            "Garantía": "📃",
            "Proveedor": "🏭",
            "Costo": "💰",
            "Responsable": "👤"
        }
        # Asegurarse de que los valores estén alineados con los campos
        for i, campo in enumerate(campos):
            col = 0 if i < 6 else 2
            row = i if i < 6 else i - 6
            emoji = iconos.get(campo, "")
            label = tk.Label(frame_formulario, text=f"{emoji} {campo}:", bg="white", anchor="w", font=("Arial", 12))
            label.grid(row=row, column=col, sticky="e", padx=20, pady=10)
            if campo == "Fecha de adquisición":
                entrada = DateEntry(frame_formulario, date_pattern='yyyy-mm-dd', width=25)
                if len(valores) == len(campos):
                    entrada.set_date(valores[i])
                else:
                    entrada.set_date("")
                entrada.grid(row=row, column=col+1, sticky="w", padx=10, pady=10)
                entradas[campo] = entrada
            elif campo == "Estado actual":
                entrada = ttk.Combobox(frame_formulario, values=["Nuevo", "Usado", "Dañado", "Baja"], state="readonly", width=28, font=("Arial", 11))
                if len(valores) == len(campos):
                    entrada.set(valores[i])
                else:
                    entrada.set("Nuevo")
                entrada.grid(row=row, column=col+1, sticky="w", padx=10, pady=10)
                entradas[campo] = entrada
            elif campo == "Garantía":
                entrada = tk.Entry(frame_formulario, width=30, font=("Arial", 11))
                if len(valores) == len(campos):
                    entrada.insert(0, valores[i])
                else:
                    entrada.insert(0, "")
                entrada.grid(row=row, column=col+1, sticky="w", padx=10, pady=10)
                entradas[campo] = entrada
            else:
                entrada = tk.Entry(frame_formulario, width=30, font=("Arial", 11))
                if len(valores) == len(campos):
                    entrada.insert(0, valores[i])
                else:
                    entrada.insert(0, "")
                entrada.grid(row=row, column=col+1, sticky="w", padx=10, pady=10)
                entradas[campo] = entrada
        def guardar_edicion():
            nuevos_datos = [entradas[c].get().strip() for c in campos]
            if not all(nuevos_datos):
                messagebox.showwarning("Campos incompletos", "Por favor completa todos los campos.")
                return
            # Ya no se fuerza a número, se permite cualquier texto en Cantidad, Costo y Garantía
            try:
                import sqlite3
                conn = sqlite3.connect('inventario.db')
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE productos SET "Numero Serial"=?, "Tipo de equipo"=?, "Marca"=?, "Modelo"=?, "Cantidad"=?, "Fecha_adquisicion"=?, "Estado_actual"=?, "Garantia"=?, "Proveedor"=?, "Costo"=?, "Responsable"=?
                    WHERE "Numero Serial"=?
                """, (
                    nuevos_datos[0], nuevos_datos[1], nuevos_datos[2], nuevos_datos[3], nuevos_datos[4], nuevos_datos[5],
                    nuevos_datos[6], nuevos_datos[7], nuevos_datos[8], nuevos_datos[9], nuevos_datos[10],
                    valores[0]
                ))
                conn.commit()
                conn.close()
                messagebox.showinfo("Éxito", "Producto editado correctamente.")
                ventana_editar.destroy()
                mostrar_productos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo editar el producto:\n{e}")
        total_filas = max(6, len(campos) - 6)
        btn_guardar = tk.Button(
            frame_formulario,
            text="💾 Guardar cambios",
            command=guardar_edicion,
            bg="#2980b9",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10
        )
        btn_guardar.grid(row=total_filas + 1, column=0, columnspan=4, pady=30)

    btn_eliminar = tk.Button(frame_acciones, text="Eliminar", command=eliminar_producto, bg="#e74c3c", fg="white", font=("Arial", 11, "bold"), width=16, height=2)
    btn_eliminar.pack(side="left", padx=5)
    btn_editar = tk.Button(frame_acciones, text="Editar", command=editar_producto, bg="#f39c12", fg="white", font=("Arial", 11, "bold"), width=16, height=2)
    btn_editar.pack(side="left", padx=5)

    # --- Filtrado tipo Excel en encabezados ---
    filtros_activos = {}

    def mostrar_menu_filtro(event):
        region = tabla.identify_region(event.x, event.y)
        if region == 'heading':
            col_id = tabla.identify_column(event.x)
            col_idx = int(col_id.replace('#', '')) - 1
            col_name = columnas[col_idx]
            import sqlite3
            conn = sqlite3.connect('inventario.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM productos')
            productos = cursor.fetchall()
            opciones = sorted(set(str(prod[col_idx]) for prod in productos))
            conn.close()
            menu = tk.Menu(tabla, tearoff=0)
            menu.add_command(label="(Quitar filtro)", command=lambda: quitar_filtro(col_idx))
            for valor in opciones:
                menu.add_command(label=str(valor), command=lambda v=valor: aplicar_filtro(col_idx, v))
            menu.tk_popup(event.x_root, event.y_root)

    def aplicar_filtro(idx, valor):
        filtros_activos[idx] = valor
        actualizar_tabla_filtrada()

    def quitar_filtro(idx):
        if idx in filtros_activos:
            del filtros_activos[idx]
        actualizar_tabla_filtrada()

    def actualizar_tabla_filtrada():
        for row in tabla.get_children():
            tabla.delete(row)
        import sqlite3
        conn = sqlite3.connect('inventario.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM productos')
        productos = cursor.fetchall()
        for prod in productos:
            cumple = True
            for idx, val in filtros_activos.items():
                if str(prod[idx]) != str(val):
                    cumple = False
                    break
            if cumple:
                tabla.insert('', 'end', values=prod[:-1])
        conn.close()

    tabla.bind('<Button-3>', mostrar_menu_filtro)

    # Mostrar todos los productos al iniciar
    mostrar_productos()
    root.mainloop()

# Mostrar login antes de la app principal
if __name__ == "__main__":
    root_login = tk.Tk()
    root_login.withdraw()

    def on_login_exitoso():
        root_login.destroy()
        iniciar_ventana_inventario()

    mostrar_login(root_login, on_login_exitoso)
    root_login.mainloop()
