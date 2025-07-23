import os
import ctypes
import sqlite3
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

BASE_DIR = os.path.dirname(__file__)
DB_NAME = "inventario.db"
FONDO_PATH = os.path.join(BASE_DIR, "login_fondo.png")

ICONO_USER_PATH = os.path.join(BASE_DIR, "icono_usuario.png")
ICONO_EMAIL_PATH = os.path.join(BASE_DIR, "icono_email.png")
ICONO_PASS_PATH = os.path.join(BASE_DIR, "icono_contrasena.png")
ICONO_CHECK_PATH = os.path.join(BASE_DIR, "icono_afirmar_contrasena.png")

def aplicar_fondo(ventana: tk.Toplevel | tk.Tk, ruta=FONDO_PATH):
    if not os.path.exists(ruta):
        return

    def _redimensionar(_event=None):
        w, h = ventana.winfo_width(), ventana.winfo_height()
        if w < 10 or h < 10:
            return
        im = Image.open(ruta).resize((w, h), Image.LANCZOS)
        tk_img = ImageTk.PhotoImage(im)
        fondo_lbl.config(image=tk_img)
        fondo_lbl.image = tk_img

    im = Image.open(ruta)
    tk_img = ImageTk.PhotoImage(im)
    fondo_lbl = tk.Label(ventana, image=tk_img)
    fondo_lbl.image = tk_img
    fondo_lbl.place(x=0, y=0, relwidth=1, relheight=1)
    fondo_lbl.lower()
    ventana.bind("<Configure>", _redimensionar)

def crear_tabla_usuarios():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                usuario    TEXT PRIMARY KEY,
                email      TEXT,
                contrasena TEXT
            )
            """
        )

def verificar_login(usuario: str, contrasena: str):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.execute("SELECT contrasena FROM usuarios WHERE usuario = ?", (usuario,))
        row = cur.fetchone()
    if row is None:
        return "no_usuario"
    return row[0] == contrasena

def mostrar_login(root: tk.Tk, on_login_exitoso):
    crear_tabla_usuarios()

    login_win = tk.Toplevel(root)
    login_win.title("LOGIN")
    login_win.state("zoomed")
    login_win.grab_set()
    login_win.configure(bg="#e0e7ef")
    aplicar_fondo(login_win)

    frame_form = tk.Frame(login_win, bg="white", bd=2, relief="groove")
    frame_form.place(relx=0.5, rely=0.5, anchor="center", width=400, height=400)

    tk.Label(frame_form, text="INVENTA QR", font=("Arial", 16, "bold"), bg="white").pack(pady=8)
    tk.Label(frame_form, text="Nombre de usuario:", bg="white").pack(pady=(5, 0))

    icono_usuario_path = os.path.join(BASE_DIR, "icono_usuario.png")
    icono_contra_path = os.path.join(BASE_DIR, "icono_contrasena.png")

    icono_usuario = ImageTk.PhotoImage(Image.open(icono_usuario_path)) if os.path.exists(icono_usuario_path) else None
    icono_contra = ImageTk.PhotoImage(Image.open(icono_contra_path).resize((24, 24), Image.LANCZOS)) if os.path.exists(icono_contra_path) else None

    frame_usuario = tk.Frame(frame_form, bg="white")
    frame_usuario.pack(pady=3)
    if icono_usuario:
        lbl_icono_u = tk.Label(frame_usuario, image=icono_usuario, bg="white")
        lbl_icono_u.image = icono_usuario
        lbl_icono_u.pack(side="left", padx=(0, 5))

    entry_usuario = tk.Entry(frame_usuario, bg="white")
    entry_usuario.pack(side="left", fill="x", expand=True)

    tk.Label(frame_form, text="Contraseña:", bg="white").pack(pady=(5, 0))
    frame_contra = tk.Frame(frame_form, bg="white")
    frame_contra.pack(pady=3)

    if icono_contra:
        lbl_icono_c = tk.Label(frame_contra, image=icono_contra, bg="white")
        lbl_icono_c.image = icono_contra
        lbl_icono_c.pack(side="left", padx=(0, 5))

    entry_contrasena = tk.Entry(frame_contra, show="*", bg="white")
    entry_contrasena.pack(side="left", fill="x", expand=True)

    def intentar_login():
        usuario = entry_usuario.get().strip()
        contrasena = entry_contrasena.get()
        resultado = verificar_login(usuario, contrasena)
        if resultado is True:
            # Guardar usuario activo en root_login para acceso global
            root.usuario_activo = usuario
            if hasattr(root, 'usuario_activo'):
                root.usuario_activo = usuario
            login_win.master.usuario_activo = usuario
            login_win.destroy()
            on_login_exitoso()
        elif resultado == "no_usuario":
            messagebox.showerror("Usuario no registrado", "El usuario ingresado no está registrado.", parent=login_win)
        else:
            messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos.", parent=login_win)

    btn_login = tk.Button(frame_form, text="INICIAR SESIÓN", command=intentar_login, bg="#3949ab", fg="white")
    btn_login.pack(pady=10)

    tk.Label(frame_form, text="¿No tienes cuenta?", bg="white", fg="#1a237e").pack(pady=(10, 0))

    def abrir_registro():
        registro_win = tk.Toplevel(root)
        registro_win.title("REGISTRO DE CUENTA")
        registro_win.geometry("500x500")
        registro_win.configure(bg="#e0e7ef")
        registro_win.grab_set()
        aplicar_fondo(registro_win)

        frame_form = tk.Frame(registro_win, bg="white", bd=2, relief="groove")
        frame_form.place(relx=0.5, rely=0.5, anchor="center", width=600, height=400)

        # Configura las columnas para que se expandan y los campos queden alineados y centrados
        frame_form.grid_columnconfigure(0, weight=1)
        frame_form.grid_columnconfigure(1, weight=1)
        frame_form.grid_columnconfigure(2, weight=2)

        tk.Label(
            frame_form, text="REGISTRO DE CUENTA", font=("Arial", 14, "bold"), bg="white"
        ).grid(row=0, column=0, columnspan=3, pady=(12, 18), sticky="ew")

        def _cargar(path):
            return (ImageTk.PhotoImage(Image.open(path).resize((24, 24), Image.LANCZOS))
                    if os.path.exists(path) else None)

        icon_user = _cargar(ICONO_USER_PATH)
        icon_email = _cargar(ICONO_EMAIL_PATH)
        icon_pass = _cargar(ICONO_PASS_PATH)
        icon_check = _cargar(ICONO_CHECK_PATH)
        
         # Mantener referencias a los iconos para que no se eliminen
        icon_refs = [icon_user, icon_email, icon_pass, icon_check]
        frame_form.icon_refs = icon_refs

        campos = [
            ("Nombre de usuario:", icon_user, tk.StringVar()),
            ("Email:", icon_email, tk.StringVar()),
            ("Contraseña:", icon_pass, tk.StringVar()),
            ("Confirmar contraseña:", icon_check, tk.StringVar()),
        ]

        entries = {}
        for i, (texto, icono, var) in enumerate(campos, start=1):
            if icono:
                tk.Label(frame_form, image=icono, bg="white").grid(row=i, column=0, padx=(0, 8), pady=6, sticky="w")
            else:
                tk.Label(frame_form, width=2, bg="white").grid(row=i, column=0, sticky="w")

            tk.Label(frame_form, text=texto, bg="white", anchor="w").grid(row=i, column=1, sticky="w")
            show_char = "*" if "Contraseña" in texto else ""
            entry = tk.Entry(frame_form, textvariable=var, show=show_char, width=26)
            entry.grid(row=i, column=2, padx=(6, 0), pady=6, sticky="ew")
            entries[texto] = entry

        lbl_requisitos = tk.Label(
            frame_form,
            text=("La contraseña debe tener al menos 8 caracteres, una mayúscula,\n"
                  "una minúscula, un número y un símbolo."),
            font=("Arial", 8), fg="red", bg="white",
            justify="left", wraplength=350
        )
        lbl_requisitos.grid(row=len(campos)+1, column=0, columnspan=3, pady=(4, 10), sticky="w")

        def registrar(registro_win=registro_win):
            import re
            usuario = entries["Nombre de usuario:"].get().strip()
            email = entries["Email:"].get().strip()
            contra = entries["Contraseña:"].get()
            confirma = entries["Confirmar contraseña:"].get()

            if not all([usuario, email, contra, confirma]):
                messagebox.showerror("Error", "Todos los campos son obligatorios", parent=registro_win)
                return
            if (len(contra) < 8 or not re.search(r"[A-Z]", contra)
                    or not re.search(r"[a-z]", contra)
                    or not re.search(r"\d", contra)
                    or not re.search(r"[^A-Za-z0-9]", contra)):
                messagebox.showerror("Error", lbl_requisitos['text'], parent=registro_win)
                return
            if contra != confirma:
                messagebox.showerror("Error", "Las contraseñas no coinciden", parent=registro_win)
                return

            with sqlite3.connect(DB_NAME) as conn:
                cur = conn.execute("SELECT 1 FROM usuarios WHERE usuario = ?", (usuario,))
                if cur.fetchone():
                    messagebox.showerror("Error", "El usuario ya existe", parent=registro_win)
                    return
                conn.execute("INSERT INTO usuarios (usuario, email, contrasena) VALUES (?, ?, ?)", (usuario, email, contra))

            messagebox.showinfo("Éxito", "Cuenta registrada correctamente", parent=registro_win)
            registro_win.destroy()

        tk.Button(frame_form, text="REGISTRAR", command=registrar, bg="#3949ab", fg="white", width=20).grid(row=len(campos)+2, column=0, columnspan=3, pady=(10, 0))

    btn_registro = tk.Button(frame_form, text="Registrarse", command=abrir_registro, bg="#3949ab", fg="white")
    btn_registro.pack(pady=5)

    login_win.protocol("WM_DELETE_WINDOW", root.destroy)