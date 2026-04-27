import json
import customtkinter as ctk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk

# ====== CONFIGURACIÓN DE TEMA AMAZÓNICO ======
ctk.set_appearance_mode("dark")

# Colores base
COLOR_BOTON = "#3E7C59"
COLOR_HOVER = "#2F5D44"
COLOR_TEXTO = "#EEDC82"
COLOR_FRAME = "#264D37"

# ====== FUNCIONES ======
def cargar_datos():
    try:
        with open("menus.json", "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return []

def guardar_datos(menus):
    with open("menus.json", "w", encoding="utf-8") as archivo:
        json.dump(menus, archivo, ensure_ascii=False, indent=4)

def mostrar_ventana(titulo, menus):
    ventana = ctk.CTkToplevel(root)
    ventana.title(titulo)
    ventana.geometry("700x600")

    frame_scroll = ctk.CTkScrollableFrame(ventana, width=650, height=500)
    frame_scroll.pack(padx=10, pady=10, fill="both", expand=True)

    imagen_refs = []

    for m in menus:
        tarjeta = ctk.CTkFrame(frame_scroll, corner_radius=10)
        tarjeta.pack(pady=10, padx=10, fill="x")

        info = (
            f"{m['Nombre']}\n"
            f"Tipo: {m['Tipo']}\n"
            f"Categoria: {m['Categoria']}\n"
            f"País: {m['País']}\n"
            f"Ingredientes: {m['Ingredientes']}\n"
            f"Dirección: {m['Dirección']}\n"
            f"Precio: {m['Precio']}\n"
        )

        etiqueta_texto = ctk.CTkLabel(tarjeta, text=info, anchor="w", justify="left")
        etiqueta_texto.pack(padx=10, pady=(10, 5))

        if "Imagen" in m and m["Imagen"]:
            try:
                img = Image.open(m["Imagen"])
                img = img.resize((200, 150))
                img_tk = ImageTk.PhotoImage(img)
                imagen_refs.append(img_tk)
                etiqueta_imagen = ctk.CTkLabel(tarjeta, image=img_tk, text="")
                etiqueta_imagen.pack(pady=(5, 10))
            except FileNotFoundError:
                ctk.CTkLabel(tarjeta, text="⚠️ Imagen no encontrada", text_color="red").pack(pady=(5, 10))

    ventana.imagen_refs = imagen_refs

def agregar_menu():
    nombre = simpledialog.askstring("Nombre", "Ingrese el nombre del restaurante:")
    tipo = simpledialog.askstring("Tipo", "Ingrese el tipo de comida:")
    categoria = simpledialog.askstring("Categoria", "Ingrese la categoria de la comida:")
    pais = simpledialog.askstring("País", "Ingrese el país de la comida:")
    ingredientes = simpledialog.askstring("Ingredientes", "Ingrese los ingredientes:")
    direccion = simpledialog.askstring("Dirección", "Ingrese la dirección del restaurante:")
    try:
        precio = int(simpledialog.askstring("Precio", "Ingrese el precio:"))
    except (ValueError, TypeError):
        messagebox.showerror("Error", "Debe ingresar un precio válido (número).")
        return

    if None in (nombre, tipo, pais, ingredientes, direccion):
        messagebox.showwarning("Faltan datos", "Todos los campos son obligatorios.")
        return

    nuevo_menu = {
        "Nombre": nombre,
        "Tipo": tipo,
        "Categoria": categoria,
        "País": pais,
        "Ingredientes": ingredientes,
        "Dirección": direccion,
        "Precio": precio
    }

    menus = cargar_datos()
    menus.append(nuevo_menu)
    guardar_datos(menus)
    messagebox.showinfo("Éxito", "Menú agregado exitosamente.")

def mostrar_datos():
    menus = cargar_datos()
    if not menus:
        messagebox.showinfo("Datos", "No hay menús disponibles.")
        return
    mostrar_ventana("Todos los Menús", menus)

def mostrar_por_pais(pais_objetivo):
    menus = cargar_datos()
    encontrados = [m for m in menus if m["País"].strip().lower() == pais_objetivo.lower()]
    if not encontrados:
        messagebox.showinfo("Resultado", f"No hay comida de {pais_objetivo}.")
        return
    mostrar_ventana(f"Comida {pais_objetivo}", encontrados)

def mostrar_categorias():
    ventana_cat = ctk.CTkToplevel(root)
    ventana_cat.title("Categorías")
    ventana_cat.geometry("350x400")

    ctk.CTkLabel(
        ventana_cat,
        text="Seleccione una categoría:",
        font=("Segoe UI", 18, "bold"),
        text_color=COLOR_TEXTO
    ).pack(pady=20)

    categorias = ["Arroces", "Carnes", "Pescado", "Sopas", "Jugos", "Fritos"]

    def filtrar_categoria(cat):
        menus = cargar_datos()
        encontrados = [m for m in menus if cat.lower() in m["Categoria"].lower()]
        if encontrados:
            mostrar_ventana(f"{cat}", encontrados)
        else:
            messagebox.showinfo("Sin resultados", f"No hay menús de {cat}.")

    for cat in categorias:
        ctk.CTkButton(
            ventana_cat,
            text=cat,
            command=lambda c=cat: filtrar_categoria(c),
            fg_color=COLOR_BOTON,
            hover_color=COLOR_HOVER,
            text_color="white",
            font=("Segoe UI Semibold", 15),
            corner_radius=10,
            height=40,
            width=200
        ).pack(pady=5)

def salir():
    root.destroy()

# ====== INTERFAZ PRINCIPAL ======
root = ctk.CTk()
root.title("DAAMANI GUYE - Sabores Ancestrales")

# *** ⬇️ Cambio para que ocupe pantalla completa ⬇️ ***
ancho_pantalla = root.winfo_screenwidth()
alto_pantalla = root.winfo_screenheight()
root.geometry(f"{ancho_pantalla}x{alto_pantalla}")

# ====== FONDO CON IMAGEN ======
try:
    fondo_img = Image.open("Fondo.jpeg")

    # *** ⬇️ Cambio para agrandar el fondo a toda la pantalla ⬇️ ***
    fondo_img = fondo_img.resize((ancho_pantalla, alto_pantalla), Image.LANCZOS)

    fondo_tk = ImageTk.PhotoImage(fondo_img)

    label_fondo = ctk.CTkLabel(root, image=fondo_tk, text="")
    label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
except Exception as e:
    messagebox.showerror("Error", f"No se pudo cargar la imagen de fondo: {e}")

# ====== LOGO ======
try:
    imagen_logo = Image.open("logo.jpg")
    imagen_logo = imagen_logo.resize((230, 230), Image.LANCZOS)
    logo = ImageTk.PhotoImage(imagen_logo)
    etiqueta_logo = ctk.CTkLabel(root, image=logo, text="")
    etiqueta_logo.image = logo
    etiqueta_logo.pack(pady=(15, 5))
except Exception as e:
    messagebox.showerror("Error", f"No se pudo cargar el logo: {e}")

# ====== TÍTULO ======
titulo = ctk.CTkLabel(
    root,
    text="DAAMANI GUYE",
    font=("Papyrus", 28, "bold"),
    text_color=COLOR_TEXTO,
    bg_color="transparent"
)
titulo.pack(pady=(0, 15))

# ====== FRAME DE BOTONES ======
frame = ctk.CTkFrame(root, fg_color="#264D37", corner_radius=15)
frame.pack(pady=20, padx=25, fill="both", expand=True)

def crear_boton(texto, comando):
    return ctk.CTkButton(
        frame,
        text=texto,
        command=comando,
        fg_color=COLOR_BOTON,
        hover_color=COLOR_HOVER,
        text_color="white",
        font=("Segoe UI Semibold", 15),
        corner_radius=12,
        height=40
    )

crear_boton("🍽 Categorías", mostrar_categorias).pack(pady=8)
crear_boton("📜 Mostrar Menús", mostrar_datos).pack(pady=8)
crear_boton("🇨🇴 Comidas Colombianas", lambda: mostrar_por_pais("Colombia")).pack(pady=8)
crear_boton("🇧🇷 Comidas Brasileras", lambda: mostrar_por_pais("Brasil")).pack(pady=8)
crear_boton("🇵🇪 Comidas Peruanas", lambda: mostrar_por_pais("Perú")).pack(pady=8)
crear_boton("➕ Agregar Menú", agregar_menu).pack(pady=8)

# ====== BOTÓN SALIR ======
ctk.CTkButton(
    root,
    text="❌ Salir",
    command=salir,
    fg_color="#B33F00",
    hover_color="#802B00",
    text_color="white",
    font=("Segoe UI", 15, "bold"),
    corner_radius=15,
    height=45
).pack(pady=20)

root.mainloop()
