import json
import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk

# ====== CONFIGURACIÓN ======
ctk.set_appearance_mode("dark")

COLOR_BOTON = "#3E7C59"
COLOR_HOVER = "#2F5D44"
COLOR_TEXTO = "#EEDC82"
COLOR_FRAME = "#264D37"

# ====== DATOS ======
def cargar_datos():
    try:
        with open("menus.json", "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except:
        return []

def guardar_datos(menus):
    with open("menus.json", "w", encoding="utf-8") as archivo:
        json.dump(menus, archivo, ensure_ascii=False, indent=4)

# ====== MOSTRAR MENÚS ======
def mostrar_ventana(titulo, menus):
    ventana = ctk.CTkToplevel(root)
    ventana.title(titulo)
    ventana.geometry("700x600")

    frame_scroll = ctk.CTkScrollableFrame(ventana)
    frame_scroll.pack(fill="both", expand=True, padx=10, pady=10)

    imagen_refs = []

    for m in menus:
        tarjeta = ctk.CTkFrame(frame_scroll)
        tarjeta.pack(pady=10, padx=10, fill="x")

        info = f"""
{m['Nombre']}
Tipo: {m['Tipo']}
Categoría: {m['Categoria']}
País: {m['País']}
Ingredientes: {m['Ingredientes']}
Dirección: {m['Dirección']}
Precio: {m['Precio']}
"""

        ctk.CTkLabel(tarjeta, text=info, justify="left").pack(padx=10, pady=5)

        if m.get("Imagen"):
            try:
                img = Image.open(m["Imagen"]).resize((200,150))
                img_tk = ImageTk.PhotoImage(img)
                imagen_refs.append(img_tk)
                ctk.CTkLabel(tarjeta, image=img_tk, text="").pack()
            except:
                ctk.CTkLabel(tarjeta, text="⚠️ Imagen no encontrada", text_color="red").pack()

    ventana.imagen_refs = imagen_refs

# ====== AGREGAR MENÚ (VENTANA PROFESIONAL) ======
def agregar_menu():
    ventana = ctk.CTkToplevel(root)
    ventana.title("Agregar Menú")
    ventana.geometry("700x600")
    ventana.grab_set()

    ctk.CTkLabel(
        ventana,
        text="🍽 REGISTRAR NUEVO MENÚ",
        font=("Segoe UI", 20, "bold"),
        text_color=COLOR_TEXTO
    ).pack(pady=10)

    frame = ctk.CTkFrame(ventana, fg_color=COLOR_FRAME, corner_radius=15)
    frame.pack(fill="both", expand=True, padx=20, pady=10)

    campos = {}

    def crear_campo(texto):
        ctk.CTkLabel(frame, text=texto).pack(pady=(10,0), padx=10, anchor="w")
        entry = ctk.CTkEntry(frame)
        entry.pack(pady=5, padx=10, fill="x")
        campos[texto] = entry

    for campo in ["Nombre","Tipo","Categoria","País","Ingredientes","Dirección","Precio","Imagen"]:
        crear_campo(campo)

    def guardar():
        try:
            precio = int(campos["Precio"].get())
        except:
            messagebox.showerror("Error","Precio inválido")
            return

        nuevo = {k:campos[k].get() for k in campos}
        nuevo["Precio"] = precio

        datos = cargar_datos()
        datos.append(nuevo)
        guardar_datos(datos)

        messagebox.showinfo("Éxito","Menú agregado")
        ventana.destroy()

    ctk.CTkButton(frame, text="Guardar", command=guardar).pack(pady=15)

# ====== EDITAR ======
def editar_menu(index):
    datos = cargar_datos()
    m = datos[index]

    ventana = ctk.CTkToplevel(root)
    ventana.title("Editar Menú")
    ventana.geometry("500x500")

    frame = ctk.CTkFrame(ventana)
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    vars = {}

    for key in m:
        ctk.CTkLabel(frame, text=key).pack()
        var = ctk.StringVar(value=str(m[key]))
        entry = ctk.CTkEntry(frame, textvariable=var)
        entry.pack(pady=5, fill="x")
        vars[key] = var

    def guardar():
        try:
            vars["Precio"].set(int(vars["Precio"].get()))
        except:
            messagebox.showerror("Error","Precio inválido")
            return

        datos[index] = {k:vars[k].get() for k in vars}
        datos[index]["Precio"] = int(datos[index]["Precio"])

        guardar_datos(datos)
        messagebox.showinfo("Éxito","Actualizado")
        ventana.destroy()

    ctk.CTkButton(frame, text="Guardar cambios", command=guardar).pack(pady=10)

# ====== GESTIONAR ======
def gestionar_menus():
    ventana = ctk.CTkToplevel(root)
    ventana.title("Gestionar Menús")
    ventana.geometry("700x600")

    frame = ctk.CTkScrollableFrame(ventana)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    datos = cargar_datos()

    def refrescar():
        ventana.destroy()
        gestionar_menus()

    for i, m in enumerate(datos):
        tarjeta = ctk.CTkFrame(frame)
        tarjeta.pack(pady=10, fill="x")

        texto = f"{m['Nombre']} - {m['Categoria']} - {m['País']}"
        ctk.CTkLabel(tarjeta, text=texto).pack()

        btns = ctk.CTkFrame(tarjeta)
        btns.pack()

        ctk.CTkButton(btns, text="✏️ Editar", command=lambda i=i: editar_menu(i)).pack(side="left", padx=5)

        def eliminar(i=i):
            if messagebox.askyesno("Confirmar","¿Eliminar?"):
                d = cargar_datos()
                d.pop(i)
                guardar_datos(d)
                refrescar()

        ctk.CTkButton(btns, text="🗑 Eliminar", fg_color="#B33F00",
                      hover_color="#802B00", command=eliminar).pack(side="left", padx=5)
        
                # 🔹 BOTÓN GENERAL DE ACEPTAR CAMBIOS
    botones = ctk.CTkFrame(ventana, fg_color="transparent")
    botones.pack(pady=10)

    ctk.CTkButton(
        botones,
        text="Aceptar cambios",
        command=ventana.destroy,
        fg_color=COLOR_BOTON,
        hover_color=COLOR_HOVER
    ).pack(side="left", padx=10)

    ctk.CTkButton(
        botones,
        text="Cancelar",
        command=ventana.destroy,
        fg_color="#B33F00",
        hover_color="#802B00"
    ).pack(side="left", padx=10)

# ====== OTROS ======
def mostrar_datos():
    datos = cargar_datos()
    if not datos:
        messagebox.showinfo("Datos", "No hay menús disponibles.")
        return
    mostrar_ventana("Menús", datos)

def mostrar_por_pais(p):
    datos = [m for m in cargar_datos() if m["País"].lower()==p.lower()]
    if datos:
        mostrar_ventana(p, datos)

def mostrar_categorias():
    ventana = ctk.CTkToplevel(root)
    ventana.title("Categorías")

    categorias = ["Arroces","Carnes","Pescado","Sopas","Jugos","Fritos"]

    for cat in categorias:
        ctk.CTkButton(
            ventana,
            text=cat,
            command=lambda c=cat: mostrar_ventana(c, [m for m in cargar_datos() if c.lower() in m["Categoria"].lower()])
        ).pack(pady=5)

def salir():
    root.destroy()

# ====== LOGIN ======
def cargar_usuarios():
    try:
        with open("usuarios.json","r",encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def validar(u,p):
    return any(x["username"]==u and x["password"]==p for x in cargar_usuarios())

def mostrar_login():
    win = ctk.CTkToplevel(root)
    win.geometry("300x250")

    u = ctk.CTkEntry(win, placeholder_text="Usuario")
    u.pack(pady=10)

    p = ctk.CTkEntry(win, placeholder_text="Contraseña", show="*")
    p.pack(pady=10)

    def entrar():
        if validar(u.get(),p.get()):
            win.destroy()
            root.deiconify()
        else:
            messagebox.showerror("Error","Incorrecto")

    ctk.CTkButton(win, text="Ingresar", command=entrar).pack(pady=20)
    win.protocol("WM_DELETE_WINDOW", root.destroy)

# ====== INTERFAZ PRINCIPAL ======
root = ctk.CTk()
root.title("DAAMANI GUYE - Sabores Ancestrales")
root.geometry("480x700")

# ====== FONDO ======
try:
    fondo = Image.open("Fondo.jpeg").resize((480,700))
    fondo_tk = ImageTk.PhotoImage(fondo)
    ctk.CTkLabel(root, image=fondo_tk, text="").place(relwidth=1, relheight=1)
except:
    pass

# ====== LOGO ======
try:
    logo_img = Image.open("logo.jpg").resize((230,230))
    logo = ImageTk.PhotoImage(logo_img)
    ctk.CTkLabel(root, image=logo, text="").pack(pady=10)
except:
    pass

ctk.CTkLabel(root, text="DAAMANI GUYE",
             font=("Papyrus",28,"bold"),
             text_color=COLOR_TEXTO).pack()

frame = ctk.CTkFrame(root, fg_color=COLOR_FRAME)
frame.pack(expand=True, fill="both", padx=20, pady=20)

def btn(t,c):
    return ctk.CTkButton(frame,text=t,command=c,
                         fg_color=COLOR_BOTON,
                         hover_color=COLOR_HOVER)

btn("🍽 Categorías", mostrar_categorias).pack(pady=5)
btn("📜 Mostrar Menús", mostrar_datos).pack(pady=5)
btn("🇨🇴 Colombia", lambda: mostrar_por_pais("Colombia")).pack(pady=5)
btn("🇧🇷 Brasil", lambda: mostrar_por_pais("Brasil")).pack(pady=5)
btn("🇵🇪 Perú", lambda: mostrar_por_pais("Perú")).pack(pady=5)
btn("➕ Agregar Menú", agregar_menu).pack(pady=5)
btn("⚙️ Gestionar Menús", gestionar_menus).pack(pady=5)

ctk.CTkButton(root,text="❌ Salir",command=salir,
              fg_color="#B33F00").pack(pady=10)

root.withdraw()
mostrar_login()
root.mainloop()