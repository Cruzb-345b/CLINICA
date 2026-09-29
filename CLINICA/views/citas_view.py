"""
views/citas_view.py
Vista del módulo Citas: formulario con validación de FK + tabla Treeview.
"""

import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox

from config import (
    COLOR_BG, COLOR_CARD, COLOR_SUCCESS, COLOR_DANGER, COLOR_WARNING,
    COLOR_TEXT, FONT_SUBTITLE, COLOR_ENTRY_BORDER,
)
from controllers.citas_controller import CitasController
from views.base_view import BaseView


class CitasView(BaseView):
    """Frame del módulo Citas."""

    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.controller = CitasController(app.db)
        self._construir()

    def _construir(self):
        """Construye toda la interfaz de citas."""
        self.crear_header("Gestión de Citas", "📅", "ico_citas")

        # --- Formulario ---
        card_form = ctk.CTkFrame(self.scroll_frame, fg_color=COLOR_CARD, corner_radius=10, border_width=1, border_color=COLOR_ENTRY_BORDER)
        card_form.pack(fill="x", padx=30, pady=(0, 20))

        ctk.CTkLabel(card_form, text="Nueva Cita", font=FONT_SUBTITLE,
                 text_color=COLOR_TEXT).grid(
            row=0, column=0, columnspan=4, sticky="w", pady=(10, 10), padx=20)

        campos_izq = ctk.CTkFrame(card_form, fg_color="transparent")
        campos_izq.grid(row=1, column=0, sticky="nsew", padx=(20, 20))
        campos_izq.columnconfigure(1, weight=1)

        campos_der = ctk.CTkFrame(card_form, fg_color="transparent")
        campos_der.grid(row=1, column=1, sticky="nsew", padx=(0, 20))
        campos_der.columnconfigure(1, weight=1)

        card_form.columnconfigure(0, weight=1)
        card_form.columnconfigure(1, weight=1)

        self.entry_id_cita = self.crear_entry(campos_izq, "ID Cita:", 0)
        self.entry_id_medico = self.crear_entry(campos_izq, "ID Médico:", 1)
        self.entry_id_paciente = self.crear_entry(campos_izq, "ID Paciente:", 2)
        self.entry_id_consultorio = self.crear_entry(campos_der, "ID Consultorio:", 0)
        self.entry_fecha = self.crear_entry(campos_der, "Fecha (YYYY-MM-DD):", 1)
        self.entry_hora = self.crear_entry(campos_der, "Hora (HH:MM:SS):", 2)

        self._entries = [
            self.entry_id_cita, self.entry_id_medico, self.entry_id_paciente,
            self.entry_id_consultorio, self.entry_fecha, self.entry_hora,
        ]

        # Botones de acción
        frame_btns = ctk.CTkFrame(card_form, fg_color="transparent")
        frame_btns.grid(row=2, column=0, columnspan=4, pady=(20, 20), padx=20, sticky="w")

        self.crear_boton(frame_btns, "💾 Registrar Cita", self._registrar,
                         COLOR_SUCCESS, "#16a34a").pack(side="left", padx=(0, 10))
        self.crear_boton(frame_btns, "🗑️ Eliminar Cita", self._eliminar,
                         COLOR_DANGER, "#dc2626").pack(side="left")

        # --- Barra de Búsqueda ---
        self.crear_barra_busqueda(
            self.scroll_frame, 
            "Buscar por ID Cita o Nombres...", 
            self._buscar, 
            self._refrescar
        )

        # --- Tabla ---
        columnas = ("ID Cita", "Médico", "Paciente", "Consultorio", "Fecha", "Hora")
        anchos = (70, 160, 160, 90, 120, 100)
        self.tree = self.crear_treeview(self.scroll_frame, columnas, anchos)

        # --- Botones Exportar y PDF ---
        frame_export = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        frame_export.pack(fill="x", padx=30, pady=(0, 30))
        
        self.crear_boton(
            frame_export, "📥 Exportar a Excel", 
            lambda: self.exportar_excel(self.tree, "reporte_citas"),
            is_secondary=True
        ).pack(side="right", padx=(10, 0))
        
        self.crear_boton(
            frame_export, "📄 Generar Ticket PDF",
            self._generar_pdf,
            is_secondary=True
        ).pack(side="right")

        self._refrescar()

    # --------------------------------------------------------
    #  ACCIONES
    # --------------------------------------------------------
    def _limpiar_campos(self):
        for e in self._entries:
            e.delete(0, tk.END)

    def _generar_pdf(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione una cita de la tabla para generar el PDF.", parent=self.app)
            return
            
        valores = self.tree.item(seleccion[0], "values")
        id_cita = valores[0]
        
        ok, msg = self.controller.generar_ticket_pdf(id_cita)
        if ok:
            messagebox.showinfo("Éxito", f"Ticket PDF generado correctamente:\n{msg}", parent=self.app)
        else:
            messagebox.showerror("Error", f"No se pudo generar el PDF:\n{msg}", parent=self.app)

    def _buscar(self, termino):
        if not termino.strip():
            self._refrescar()
            return
        datos = self.controller.buscar(termino.strip())
        self.llenar_treeview(self.tree, datos)

    def _refrescar(self):
        datos = self.controller.listar()
        self.llenar_treeview(self.tree, datos)

    def _registrar(self):
        id_c = self.entry_id_cita.get().strip()
        id_m = self.entry_id_medico.get().strip()
        id_p = self.entry_id_paciente.get().strip()
        id_cons = self.entry_id_consultorio.get().strip()
        fecha = self.entry_fecha.get().strip()
        hora = self.entry_hora.get().strip()

        if not all([id_c, id_m, id_p, id_cons, fecha, hora]):
            messagebox.showwarning("Campos vacíos",
                                   "Todos los campos son obligatorios.", parent=self.app)
            return

        try:
            id_c = int(id_c)
            id_m = int(id_m)
            id_p = int(id_p)
            id_cons = int(id_cons)
        except ValueError:
            messagebox.showerror("Error",
                                 "Los campos ID deben ser números enteros.", parent=self.app)
            return

        # Delegar validación y registro al controller
        resultado = self.controller.registrar(id_c, id_m, id_p, id_cons, fecha, hora)

        if resultado["ok"]:
            messagebox.showinfo("Éxito", "✅ Cita registrada correctamente.",
                                parent=self.app)
            self._limpiar_campos()
            self._refrescar()
        else:
            # Título según tipo de error
            titulos = {
                "medico_no_encontrado": "Médico no encontrado",
                "paciente_no_encontrado": "Paciente no encontrado",
                "error_insercion": "Error",
            }
            titulo = titulos.get(resultado["tipo"], "Error")
            messagebox.showerror(titulo, resultado["error"], parent=self.app)

    def _eliminar(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selección",
                                   "Seleccione una cita de la tabla.", parent=self.app)
            return
        valores = self.tree.item(sel[0], "values")
        id_c = valores[0]
        confirm = messagebox.askyesno("Confirmar",
                                      f"¿Eliminar cita ID {id_c}?", parent=self.app)
        if confirm:
            ok = self.controller.eliminar(id_c)
            if ok:
                messagebox.showinfo("Éxito", "Cita eliminada.", parent=self.app)
                self._refrescar()
            else:
                messagebox.showerror("Error",
                                     "No se pudo eliminar. Puede tener historial "
                                     "clínico asociado.", parent=self.app)
