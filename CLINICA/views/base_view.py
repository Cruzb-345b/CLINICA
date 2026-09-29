import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
import customtkinter as ctk

from config import (
    BASE_DIR, COLOR_BG, COLOR_CARD, COLOR_ENTRY_BG, COLOR_ENTRY_BORDER,
    COLOR_PRIMARY, COLOR_PRIMARY_HOVER, COLOR_TEXT,
    COLOR_TEXT_SEC, COLOR_TABLE_BG, COLOR_TABLE_STRIPE, COLOR_TABLE_FG, COLOR_TABLE_SEL,
    FONT_TITLE, FONT_BODY, FONT_BUTTON,
)


class BaseView(ctk.CTkScrollableFrame):
    """
    Frame base reutilizable para todas las vistas del sistema.
    Utiliza CTkScrollableFrame para manejar el scroll automáticamente.
    """

    def __init__(self, parent, app):
        super().__init__(parent, fg_color=COLOR_BG, corner_radius=0)
        self.app = app
        self.pack(fill="both", expand=True)

        self.scroll_frame = self

    # --------------------------------------------------------
    #  HELPERS DE UI
    # --------------------------------------------------------
    def crear_header(self, titulo, icono="", imagen_key=None):
        """Crea un encabezado minimalista con título y separador sutil."""
        frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        frame.pack(fill="x", padx=30, pady=(30, 10))

        row = ctk.CTkFrame(frame, fg_color="transparent")
        row.pack(fill="x")

        # Ícono de imagen si hay
        ico = self.app.imagenes.get(imagen_key) if imagen_key else None
        if ico:
            ctk.CTkLabel(row, image=ico, text="").pack(side="left", padx=(0, 15))

        ctk.CTkLabel(row, text=f"{icono}  {titulo}", font=FONT_TITLE,
                     text_color=COLOR_TEXT).pack(side="left", anchor="w")

        # Línea divisoria sutil (1px gris tenue)
        ctk.CTkFrame(self.scroll_frame, fg_color="#333333", height=1).pack(fill="x", padx=30, pady=(5, 20))

        return frame

    def crear_entry(self, parent, label_text, row):
        """Crea un par CTkLabel + CTkEntry dentro de un grid."""
        ctk.CTkLabel(
            parent, text=label_text, font=FONT_BODY,
            text_color=COLOR_TEXT_SEC, anchor="w",
        ).grid(row=row, column=0, sticky="w", padx=(0, 15), pady=8)
        
        entry = ctk.CTkEntry(
            parent, font=FONT_BODY, fg_color=COLOR_ENTRY_BG,
            text_color=COLOR_TEXT, border_color=COLOR_ENTRY_BORDER,
            corner_radius=8, border_width=1
        )
        entry.grid(row=row, column=1, sticky="ew", pady=8, ipady=4)
        return entry

    def bloquear_entry(self, entry):
        """Pone un Entry en modo readonly o disabled."""
        entry.configure(state="readonly", fg_color="#1a1a1a")

    def desbloquear_entry(self, entry):
        """Restaura un Entry a modo normal."""
        entry.configure(state="normal", fg_color=COLOR_ENTRY_BG)

    def crear_boton(self, parent, texto, comando, color=COLOR_PRIMARY, hover=COLOR_PRIMARY_HOVER, is_secondary=False):
        """Crea un CTkButton. is_secondary=True lo hace transparente con borde."""
        if is_secondary:
            return ctk.CTkButton(
                parent, text=texto, font=FONT_BUTTON,
                fg_color="transparent", border_width=1, border_color=COLOR_ENTRY_BORDER,
                text_color=COLOR_TEXT, hover_color="#333333", corner_radius=8,
                command=comando
            )
        else:
            return ctk.CTkButton(
                parent, text=texto, font=FONT_BUTTON,
                fg_color=color, hover_color=hover,
                text_color="white", corner_radius=8,
                command=comando
            )

    def crear_treeview(self, parent, columnas, anchos):
        """Crea un Treeview estilizado minimalista con scrollbar."""
        frame_tabla = ctk.CTkFrame(parent, fg_color=COLOR_CARD, corner_radius=8, border_width=1, border_color=COLOR_ENTRY_BORDER)
        frame_tabla.pack(fill="both", expand=True, padx=30, pady=(0, 30))

        # Configurar el estilo del Treeview para CTK/Minimalista
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Minimal.Treeview",
                        background=COLOR_TABLE_BG,
                        foreground=COLOR_TABLE_FG,
                        fieldbackground=COLOR_TABLE_BG,
                        borderwidth=0,
                        rowheight=30,
                        font=FONT_BODY)
        style.map('Minimal.Treeview', background=[('selected', COLOR_TABLE_SEL)])
        style.configure("Minimal.Treeview.Heading",
                        background=COLOR_CARD,
                        foreground=COLOR_TEXT_SEC,
                        borderwidth=0,
                        font=("Roboto", 11, "bold"))
        style.map("Minimal.Treeview.Heading", background=[('active', COLOR_CARD)])

        scroll = ctk.CTkScrollbar(frame_tabla, orientation="vertical")
        tree = ttk.Treeview(
            frame_tabla, columns=columnas, show="headings",
            style="Minimal.Treeview", yscrollcommand=scroll.set,
        )
        scroll.configure(command=tree.yview)
        scroll.pack(side="right", fill="y", pady=2)
        tree.pack(fill="both", expand=True, padx=2, pady=2)

        for col, ancho in zip(columnas, anchos):
            tree.heading(col, text=col, anchor="center")
            tree.column(col, width=ancho, anchor="center")

        # Tags para filas alternas (sutiles)
        tree.tag_configure("par", background=COLOR_TABLE_BG)
        tree.tag_configure("impar", background="#333333")

        return tree

    def llenar_treeview(self, tree, datos):
        """Limpia y rellena un Treeview con datos, aplicando filas alternas."""
        for item in tree.get_children():
            tree.delete(item)
        for i, fila in enumerate(datos):
            tag = "par" if i % 2 == 0 else "impar"
            tree.insert("", "end", values=fila, tags=(tag,))

    def crear_barra_busqueda(self, parent, placeholder_text, comando_buscar, comando_limpiar):
        """Crea una barra de búsqueda minimalista."""
        frame_busqueda = ctk.CTkFrame(parent, fg_color="transparent")
        frame_busqueda.pack(fill="x", padx=30, pady=(0, 20))

        entry_buscar = ctk.CTkEntry(
            frame_busqueda, font=FONT_BODY, placeholder_text=placeholder_text,
            width=300, fg_color=COLOR_ENTRY_BG, border_color=COLOR_ENTRY_BORDER,
            corner_radius=8, border_width=1
        )
        entry_buscar.pack(side="left", padx=(0, 10))

        self.crear_boton(
            frame_busqueda, "Buscar", 
            lambda: comando_buscar(entry_buscar.get()),
            COLOR_PRIMARY, COLOR_PRIMARY_HOVER
        ).pack(side="left", padx=(0, 10))

        self.crear_boton(
            frame_busqueda, "Limpiar Filtro", 
            lambda: [entry_buscar.delete(0, tk.END), comando_limpiar()],
            is_secondary=True
        ).pack(side="left")

        return entry_buscar

    def exportar_excel(self, tree, nombre_archivo):
        """Exporta los datos de un Treeview a un archivo de Excel (.xlsx)."""
        columnas = [tree.heading(c)["text"] for c in tree["columns"]]
        datos = []
        for item in tree.get_children():
            datos.append(tree.item(item)["values"])
        
        if not datos:
            messagebox.showwarning("Exportar", "No hay datos para exportar.")
            return

        try:
            df = pd.DataFrame(datos, columns=columnas)
            ruta = os.path.join(BASE_DIR, f"{nombre_archivo}.xlsx")
            df.to_excel(ruta, index=False)
            messagebox.showinfo("Exportar Excel", f"Reporte guardado exitosamente en:\n{ruta}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el reporte:\n{e}")
