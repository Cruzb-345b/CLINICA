"""
views/pacientes_view.py
Vista CRUD del módulo Pacientes: formulario + tabla Treeview.
"""

import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox

from config import (
    COLOR_BG, COLOR_CARD, COLOR_PRIMARY, COLOR_PRIMARY_HOVER,
    COLOR_SUCCESS, COLOR_DANGER, COLOR_WARNING, COLOR_TEXT,
    FONT_SUBTITLE, COLOR_ENTRY_BORDER,
)
from controllers.pacientes_controller import PacientesController
from views.base_view import BaseView


class PacientesView(BaseView):
    """Frame del módulo Pacientes."""

    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.controller = PacientesController(app.db)
        self._construir()

    def _construir(self):
        """Construye toda la interfaz de pacientes."""
        self.crear_header("Gestión de Pacientes", "👤", "ico_pacientes")

        # --- Formulario ---
        card_form = ctk.CTkFrame(self.scroll_frame, fg_color=COLOR_CARD, corner_radius=10, border_width=1, border_color=COLOR_ENTRY_BORDER)
        card_form.pack(fill="x", padx=30, pady=(0, 20))

        ctk.CTkLabel(card_form, text="Nuevo Paciente", font=FONT_SUBTITLE,
                 text_color=COLOR_TEXT).grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(10, 10), padx=20)

        campos_frame = ctk.CTkFrame(card_form, fg_color="transparent")
        campos_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=(20, 20))
        campos_frame.columnconfigure(1, weight=1)

        self.entry_id = self.crear_entry(campos_frame, "ID Paciente:", 0)
        self.entry_nombre = self.crear_entry(campos_frame, "Nombre:", 1)
        self.entry_edad = self.crear_entry(campos_frame, "Edad:", 2)

        self._entries = [self.entry_id, self.entry_nombre, self.entry_edad]

        # Botones de acción
        frame_btns = ctk.CTkFrame(card_form, fg_color="transparent")
        frame_btns.grid(row=2, column=0, columnspan=2, pady=(20, 20), padx=20, sticky="w")

        self.crear_boton(frame_btns, "💾 Registrar", self._registrar,
                         COLOR_SUCCESS, "#16a34a").pack(side="left", padx=(0, 10))
        self.crear_boton(frame_btns, "✏️ Cargar", self._cargar_seleccion,
                         COLOR_WARNING, "#d97706").pack(side="left", padx=(0, 10))
        self.crear_boton(frame_btns, "📝 Guardar Cambios", self._guardar_cambios,
                         COLOR_PRIMARY, COLOR_PRIMARY_HOVER).pack(side="left", padx=(0, 10))
        self.crear_boton(frame_btns, "🗑️ Eliminar", self._eliminar,
                         COLOR_DANGER, "#dc2626").pack(side="left", padx=(0, 10))
        self.crear_boton(frame_btns, "🗑 Limpiar", self._limpiar_campos,
                         is_secondary=True).pack(side="left")

        # --- Barra de Búsqueda ---
        self.crear_barra_busqueda(
            self.scroll_frame, 
            "Buscar por ID o Nombre...", 
            self._buscar, 
            self._refrescar
        )

        columnas = ("ID", "Nombre", "Edad")
        anchos = (100, 300, 100)
        self.tree = self.crear_treeview(self.scroll_frame, columnas, anchos)

        # --- Botón Exportar ---
        frame_export = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        frame_export.pack(fill="x", padx=30, pady=(0, 30))
        self.crear_boton(
            frame_export, "📥 Exportar a Excel", 
            lambda: self.exportar_excel(self.tree, "reporte_pacientes"),
            is_secondary=True
        ).pack(side="right")

        self._refrescar()

    # --------------------------------------------------------
    #  ACCIONES
    # --------------------------------------------------------
    def _limpiar_campos(self):
        self.desbloquear_entry(self.entry_id)
        for e in self._entries:
            e.delete(0, tk.END)

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
        id_p = self.entry_id.get().strip()
        nombre = self.entry_nombre.get().strip()
        edad = self.entry_edad.get().strip()

        if not id_p or not nombre or not edad:
            messagebox.showwarning("Campos vacíos",
                                   "Todos los campos son obligatorios.", parent=self.app)
            return
        try:
            id_p = int(id_p)
            edad = int(edad)
        except ValueError:
            messagebox.showerror("Error de formato",
                                 "ID y Edad deben ser números enteros.", parent=self.app)
            return

        ok = self.controller.registrar(id_p, nombre, edad)
        if ok:
            messagebox.showinfo("Éxito", "✅ Paciente registrado correctamente.",
                                parent=self.app)
            self._limpiar_campos()
            self._refrescar()
        else:
            messagebox.showerror("Error",
                                 "No se pudo registrar. Verifique que el ID no esté "
                                 "duplicado o que la BD esté disponible.", parent=self.app)

    def _cargar_seleccion(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selección",
                                   "Seleccione un paciente de la tabla para editar.",
                                   parent=self.app)
            return
        valores = self.tree.item(sel[0], "values")
        self._limpiar_campos()
        self.entry_id.insert(0, valores[0])
        self.bloquear_entry(self.entry_id)
        self.entry_nombre.insert(0, valores[1])
        self.entry_edad.insert(0, valores[2])

    def _guardar_cambios(self):
        id_p = self.entry_id.get().strip()
        nombre = self.entry_nombre.get().strip()
        edad = self.entry_edad.get().strip()

        if not id_p or not nombre or not edad:
            messagebox.showwarning("Campos vacíos",
                                   "Todos los campos son obligatorios.", parent=self.app)
            return
        try:
            id_p = int(id_p)
            edad = int(edad)
        except ValueError:
            messagebox.showerror("Error de formato",
                                 "ID y Edad deben ser números enteros.", parent=self.app)
            return

        ok = self.controller.actualizar(id_p, nombre, edad)
        if ok:
            messagebox.showinfo("Éxito", "✅ Paciente actualizado.", parent=self.app)
            self._limpiar_campos()
            self._refrescar()
        else:
            messagebox.showerror("Error", "No se pudo actualizar.", parent=self.app)

    def _eliminar(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selección",
                                   "Seleccione un paciente de la tabla para eliminar.",
                                   parent=self.app)
            return
        valores = self.tree.item(sel[0], "values")
        id_p = valores[0]
        confirm = messagebox.askyesno("Confirmar",
                                      f"¿Eliminar paciente ID {id_p} - {valores[1]}?",
                                      parent=self.app)
        if confirm:
            ok = self.controller.eliminar(id_p)
            if ok:
                messagebox.showinfo("Éxito", "Paciente eliminado.", parent=self.app)
                self._refrescar()
            else:
                messagebox.showerror("Error",
                                     "No se pudo eliminar. Puede tener citas asociadas.",
                                     parent=self.app)
