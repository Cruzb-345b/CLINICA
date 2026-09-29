"""
views/dashboard_view.py
Vista del Dashboard: banner hero, tarjetas de resumen y tabla de últimas citas.
"""

import tkinter as tk
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from config import (
    COLOR_BG, COLOR_CARD, COLOR_PRIMARY, COLOR_SUCCESS,
    COLOR_WARNING, COLOR_PURPLE, COLOR_TEXT, COLOR_TEXT_SEC, COLOR_ENTRY_BORDER,
    FONT_SUBTITLE, FONT_BODY, FONT_SMALL, FONT_ICON,
)
from controllers.dashboard_controller import DashboardController
from views.base_view import BaseView


class DashboardView(BaseView):
    """Frame del módulo Dashboard."""

    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.controller = DashboardController(app.db)
        self._construir()

    def _construir(self):
        """Construye toda la interfaz del dashboard."""
        self._crear_banner()
        self._crear_tarjetas()
        self._crear_graficos()
        self._crear_tabla_citas()

    # --------------------------------------------------------
    #  BANNER HERO
    # --------------------------------------------------------
    def _crear_banner(self):
        # Banner minimalista, se usa el header de BaseView en vez del banner recargado
        self.crear_header("Dashboard", "📊")

    # --------------------------------------------------------
    #  TARJETAS DE RESUMEN
    # --------------------------------------------------------
    def _crear_tarjetas(self):
        frame_cards = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        frame_cards.pack(fill="x", padx=30, pady=(0, 20))

        datos_cards = [
            ("ico_pacientes", "👤", "Pacientes",
             self.controller.obtener_conteo_pacientes, COLOR_PRIMARY),
            ("ico_medicos", "🩺", "Médicos",
             self.controller.obtener_conteo_medicos, COLOR_SUCCESS),
            ("ico_citas", "📅", "Citas",
             self.controller.obtener_conteo_citas, COLOR_WARNING),
            ("ico_dashboard", "👩‍⚕️", "Enfermeras",
             self.controller.obtener_conteo_enfermeras, COLOR_PURPLE),
        ]

        for i, (ico_key, fallback, titulo, fn_conteo, color) in enumerate(datos_cards):
            cantidad = fn_conteo()

            card = ctk.CTkFrame(frame_cards, fg_color=COLOR_CARD, corner_radius=10,
                                border_width=1, border_color=COLOR_ENTRY_BORDER)
            card.grid(row=0, column=i, padx=8, pady=4, sticky="nsew")
            frame_cards.columnconfigure(i, weight=1)

            # Fila superior: ícono + número
            top_row = ctk.CTkFrame(card, fg_color="transparent")
            top_row.pack(fill="x", padx=20, pady=(20, 5))

            ico = self.app.imagenes.get(ico_key)
            if ico:
                ctk.CTkLabel(top_row, image=ico, text="").pack(side="left")
            else:
                ctk.CTkLabel(top_row, text=fallback, font=FONT_ICON,
                             text_color=color).pack(side="left")

            ctk.CTkLabel(top_row, text=str(cantidad), font=("Roboto", 32, "bold"),
                         text_color=COLOR_TEXT).pack(side="right")

            # Nombre
            ctk.CTkLabel(card, text=titulo, font=FONT_BODY, text_color=COLOR_TEXT_SEC, anchor="w").pack(fill="x", padx=20, pady=(0, 20))

    # --------------------------------------------------------
    #  GRÁFICOS (MATPLOTLIB)
    # --------------------------------------------------------
    def _crear_graficos(self):
        frame_charts = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        frame_charts.pack(fill="x", padx=30, pady=(0, 20))

        # Configuración de estilo Matplotlib para modo oscuro minimalista
        import matplotlib as mpl
        mpl.rcParams.update({
            "text.color": COLOR_TEXT,
            "axes.labelcolor": COLOR_TEXT,
            "xtick.color": COLOR_TEXT_SEC,
            "ytick.color": COLOR_TEXT_SEC,
            "axes.edgecolor": COLOR_TEXT_SEC,
            "axes.facecolor": COLOR_CARD,
            "figure.facecolor": COLOR_CARD,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.spines.left": False,
            "axes.spines.bottom": False,
        })
        
        # Gráfico 1: Barras (Citas por Médico)
        frame_bar = ctk.CTkFrame(frame_charts, fg_color=COLOR_CARD, corner_radius=10, border_width=1, border_color=COLOR_ENTRY_BORDER)
        frame_bar.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        datos_bar = self.controller.obtener_citas_por_medico()
        fig_bar = Figure(figsize=(5, 3), dpi=100)
        fig_bar.subplots_adjust(bottom=0.2)
        ax_bar = fig_bar.add_subplot(111)
        if datos_bar:
            nombres = [d[0] for d in datos_bar]
            conteos = [d[1] for d in datos_bar]
            ax_bar.bar(nombres, conteos, color=COLOR_PRIMARY, width=0.6)
            ax_bar.set_title("Citas por Médico", pad=15)
            ax_bar.tick_params(axis='x', rotation=15)
            ax_bar.tick_params(axis='both', length=0) # Ocultar rayitas
        else:
            ax_bar.text(0.5, 0.5, "Sin datos", ha='center', va='center')
        
        canvas_bar = FigureCanvasTkAgg(fig_bar, master=frame_bar)
        canvas_bar.draw()
        canvas_bar.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        # Gráfico 2: Torta (Médicos por Especialidad)
        frame_pie = ctk.CTkFrame(frame_charts, fg_color=COLOR_CARD, corner_radius=10, border_width=1, border_color=COLOR_ENTRY_BORDER)
        frame_pie.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        datos_pie = self.controller.obtener_medicos_por_especialidad()
        fig_pie = Figure(figsize=(5, 3), dpi=100)
        ax_pie = fig_pie.add_subplot(111)
        if datos_pie:
            especialidades = [d[0] for d in datos_pie]
            conteos = [d[1] for d in datos_pie]
            ax_pie.pie(conteos, labels=especialidades, autopct='%1.1f%%', colors=[COLOR_SUCCESS, COLOR_WARNING, COLOR_PURPLE, COLOR_PRIMARY, "#f43f5e"])
            ax_pie.set_title("Médicos por Especialidad", pad=15)
        else:
            ax_pie.text(0.5, 0.5, "Sin datos", ha='center', va='center')
            
        canvas_pie = FigureCanvasTkAgg(fig_pie, master=frame_pie)
        canvas_pie.draw()
        canvas_pie.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    # --------------------------------------------------------
    #  TABLA DE ÚLTIMAS CITAS
    # --------------------------------------------------------
    def _crear_tabla_citas(self):
        frame_bottom = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        frame_bottom.pack(fill="both", expand=True, padx=0, pady=(0, 0))

        title_row = ctk.CTkFrame(frame_bottom, fg_color="transparent")
        title_row.pack(fill="x", padx=30, pady=(0, 10))
        ctk.CTkLabel(title_row, text="📋  Últimas Citas Registradas", font=FONT_SUBTITLE,
                     text_color=COLOR_TEXT).pack(side="left")
        ctk.CTkLabel(title_row, text="Mostrando las 10 más recientes", font=FONT_SMALL,
                     text_color=COLOR_TEXT_SEC).pack(side="right")

        columnas = ("ID", "Médico", "Paciente", "Consultorio", "Fecha", "Hora")
        anchos = (60, 140, 140, 100, 120, 100)

        tree = self.crear_treeview(frame_bottom, columnas, anchos)
        datos = self.controller.obtener_ultimas_citas()
        self.llenar_treeview(tree, datos)
