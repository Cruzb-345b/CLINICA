"""
main.py - Punto de entrada del Sistema de Gestión Clínica
Solo gestiona la ventana principal, el Sidebar y la navegación entre vistas.
"""

import os
import sys

# Asegurar que el directorio del proyecto esté en sys.path
# para que los imports funcionen sin importar desde dónde se ejecute main.py
_PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
if _PROJECT_DIR not in sys.path:
    sys.path.insert(0, _PROJECT_DIR)

import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

from config import (
    COLOR_BG, COLOR_SIDEBAR, COLOR_CARD,
    COLOR_PRIMARY, COLOR_PRIMARY_HOVER, COLOR_TEXT, COLOR_TEXT_SEC,
    COLOR_TABLE_BG, COLOR_TABLE_FG, COLOR_TABLE_SEL, COLOR_ENTRY_BORDER,
    FONT_BODY, FONT_SMALL, FONT_TITLE,

    LOGO_PATH, BANNER_PATH, ICONOS_PATH,
    cargar_imagen, crear_imagen_circular, recortar_icono,
)
from database import ConexionBD
from views import DashboardView, PacientesView, MedicosView, CitasView


class AplicacionClinica(ctk.CTk):
    """Ventana principal — Sidebar + contenedor de vistas."""

    def __init__(self):
        super().__init__()
        self.title("🏥 Sistema de Gestión Clínica")
        self.geometry("1150x720")
        self.minsize(1050, 650)
        self.configure(fg_color=COLOR_BG)

        # Conexión a base de datos (compartida por todos los controladores)
        self.db = ConexionBD()

        # Almacenar referencias de imágenes para que no sean recolectadas por GC
        self.imagenes = {}

        # Centrar ventana
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"+{x}+{y}")

        # Inicialización
        self._precargar_imagenes()
        self._configurar_estilos()
        self._crear_sidebar()

        # Contenedor de contenido (donde se montan las vistas)
        self.contenido = ctk.CTkFrame(self, fg_color=COLOR_BG, corner_radius=0)
        self.contenido.pack(side="right", fill="both", expand=True)

        # Vista activa
        self._vista_actual = None

        # Mostrar Dashboard por defecto
        self._navegar(0, DashboardView)

    # --------------------------------------------------------
    #  PRECARGAR IMÁGENES
    # --------------------------------------------------------
    def _precargar_imagenes(self):
        """Carga todas las imágenes al inicio para evitar el garbage collector."""
        self.imagenes["logo"] = crear_imagen_circular(LOGO_PATH, 100)
        self.imagenes["logo_small"] = cargar_imagen(LOGO_PATH, (40, 40))
        self.imagenes["banner"] = cargar_imagen(BANNER_PATH, (840, 180))
        # Íconos individuales de la grilla 2x2
        self.imagenes["ico_pacientes"] = recortar_icono(ICONOS_PATH, 0, (52, 52))
        self.imagenes["ico_medicos"] = recortar_icono(ICONOS_PATH, 1, (52, 52))
        self.imagenes["ico_citas"] = recortar_icono(ICONOS_PATH, 2, (52, 52))
        self.imagenes["ico_dashboard"] = recortar_icono(ICONOS_PATH, 3, (52, 52))

    # --------------------------------------------------------
    #  ESTILOS GLOBALES (ttk)
    # --------------------------------------------------------
    def _configurar_estilos(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure(
            "Custom.Treeview",
            background=COLOR_TABLE_BG, foreground=COLOR_TABLE_FG,
            fieldbackground=COLOR_TABLE_BG, rowheight=34,
            font=FONT_BODY, borderwidth=0,
        )
        style.configure(
            "Custom.Treeview.Heading",
            background=COLOR_PRIMARY, foreground="white",
            font=("Segoe UI", 11, "bold"), borderwidth=0,
            relief="flat", padding=(8, 6),
        )
        style.map("Custom.Treeview",
                   background=[("selected", COLOR_TABLE_SEL)],
                   foreground=[("selected", "white")])
        style.map("Custom.Treeview.Heading",
                   background=[("active", COLOR_PRIMARY_HOVER)])

        style.configure(
            "Custom.Vertical.TScrollbar",
            background=COLOR_SIDEBAR, troughcolor=COLOR_BG,
            arrowcolor=COLOR_TEXT_SEC, borderwidth=0,
        )

    # --------------------------------------------------------
    #  SIDEBAR
    # --------------------------------------------------------
    def _crear_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, fg_color=COLOR_SIDEBAR, width=240, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # --- Franja superior oscura ---
        top_frame = ctk.CTkFrame(self.sidebar, fg_color=COLOR_SIDEBAR, height=180, corner_radius=0)
        top_frame.pack(fill="x")
        top_frame.pack_propagate(False)

        # Logo circular
        if self.imagenes.get("logo"):
            ctk.CTkLabel(top_frame, image=self.imagenes["logo"], text="").pack(pady=(18, 6))
        else:
            ctk.CTkLabel(top_frame, text="🏥", font=("Segoe UI", 42), text_color=COLOR_PRIMARY).pack(pady=(18, 2))

        ctk.CTkLabel(top_frame, text="Clínica", font=FONT_TITLE, text_color=COLOR_TEXT).pack()
        ctk.CTkLabel(top_frame, text="Sistema de Gestión", font=FONT_SMALL, text_color=COLOR_TEXT_SEC).pack(pady=(0, 8))

        # Separador sutil
        ctk.CTkFrame(self.sidebar, fg_color="#333333", height=1).pack(fill="x", padx=24, pady=12)

        # Título sección menú
        ctk.CTkLabel(self.sidebar, text="MENÚ PRINCIPAL",
                 font=("Roboto", 10, "bold"),
                 text_color=COLOR_TEXT_SEC, anchor="w"
                 ).pack(fill="x", padx=24, pady=(0, 6))

        # --- Botones de navegación ---
        menu_items = [
            ("ico_dashboard", "  Dashboard", "📊", DashboardView),
            ("ico_pacientes", "  Pacientes", "👤", PacientesView),
            ("ico_medicos", "  Médicos", "🩺", MedicosView),
            ("ico_citas", "  Citas", "📅", CitasView),
        ]

        self._sidebar_btns = []
        for idx, (ico_key, texto, fallback, view_cls) in enumerate(menu_items):
            ico_img = self.imagenes.get(ico_key)
            
            btn = ctk.CTkButton(
                self.sidebar, text=texto if ico_img else f"{fallback}{texto}", font=FONT_BODY,
                image=ico_img,
                fg_color="transparent", text_color=COLOR_TEXT_SEC,
                hover_color=COLOR_CARD, anchor="w", corner_radius=8,
                command=lambda i=idx, vc=view_cls: self._navegar(i, vc)
            )
            btn.pack(fill="x", padx=16, pady=4)
            self._sidebar_btns.append(btn)

        # --- Pie de sidebar ---
        ctk.CTkFrame(self.sidebar, fg_color="transparent").pack(fill="both", expand=True)
        footer = ctk.CTkFrame(self.sidebar, fg_color="transparent", height=50)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)
        ctk.CTkLabel(footer, text="v2.0  •  INTEP 2026", font=FONT_SMALL,
                 text_color=COLOR_TEXT_SEC).pack(expand=True)

    # --------------------------------------------------------
    #  NAVEGACIÓN ENTRE VISTAS
    # --------------------------------------------------------
    def _navegar(self, idx, view_cls):
        """Destruye la vista actual y monta una nueva."""
        # Destruir vista previa
        if self._vista_actual is not None:
            self._vista_actual.destroy()

        # Resaltar botón activo
        self._set_active_btn(idx)

        # Montar nueva vista
        self._vista_actual = view_cls(self.contenido, self)

    def _set_active_btn(self, idx):
        """Resalta el botón activo del sidebar."""
        for i, btn in enumerate(self._sidebar_btns):
            if i == idx:
                btn.configure(fg_color=COLOR_PRIMARY, text_color="white")
                self._active_btn = btn
            else:
                btn.configure(fg_color="transparent", text_color=COLOR_TEXT_SEC)


# ============================================================
#  PUNTO DE ENTRADA CON LOGIN GATEKEEPER
# ============================================================
def iniciar_sistema(user, rol, root_login):
    """Callback de éxito en el login."""
    root_login.destroy()
    app = AplicacionClinica()
    app.mainloop()

if __name__ == "__main__":
    from views.login_view import LoginView
    
    root_login = ctk.CTk()
    root_login.title("Login - Clínica")
    root_login.geometry("500x550")
    
    # Centrar login
    root_login.update_idletasks()
    w, h = 500, 550
    x = (root_login.winfo_screenwidth() // 2) - (w // 2)
    y = (root_login.winfo_screenheight() // 2) - (h // 2)
    root_login.geometry(f"+{x}+{y}")
    
    # Mock para el login (necesita BD y logo)
    class AppContextLogin:
        def __init__(self):
            self.db = ConexionBD()
            self.imagenes = {
                "logo": crear_imagen_circular(LOGO_PATH, 100)
            }
            
    app_login = AppContextLogin()
    
    # Lanzar vista
    LoginView(root_login, app_login, lambda u, r: iniciar_sistema(u, r, root_login))
    root_login.mainloop()
