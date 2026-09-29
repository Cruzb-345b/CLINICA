"""
views/medicos_view.py
Vista CRUD del módulo Médicos: formulario de 2 columnas + tabla Treeview.
"""

import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox

from config import (
    COLOR_BG, COLOR_CARD, COLOR_PRIMARY, COLOR_PRIMARY_HOVER,
    COLOR_SUCCESS, COLOR_DANGER, COLOR_WARNING, COLOR_TEXT,
    FONT_SUBTITLE, COLOR_ENTRY_BORDER,
)
from controllers.medicos_controller import MedicosController
from views.base_view import BaseView


class MedicosView(BaseView):
    """Frame del módulo Médicos."""

    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.controller = MedicosController(app.db)
        self._construir()

    def _construir(self):
        """Construye toda la interfaz de médicos."""
        self.crear_header("Gestión de Médicos", "🩺", "ico_medicos")

        # --- Formulario ---
        card_form = ctk.CTkFrame(self.scroll_frame, fg_color=COLOR_CARD, corner_radius=10, border_width=1, border_color=COLOR_ENTRY_BORDER)
        card_form.pack(fill="x", padx=30, pady=(0, 20))

        ctk.CTkLabel(card_form, text="Nuevo Médico", font=FONT_SUBTITLE,
                 text_color=COLOR_TEXT).grid(
            row=0, column=0, columnspan=4, sticky="w", pady=(10, 10), padx=20)

        # Dos columnas de campos
        campos_izq = ctk.CTkFrame(card_form, fg_color="transparent")
        campos_izq.grid(row=1, column=0, sticky="nsew", padx=(20, 20))
        campos_izq.columnconfigure(1, weight=1)

        campos_der = ctk.CTkFrame(card_form, fg_color="transparent")
        campos_der.grid(row=1, column=1, sticky="nsew", padx=(0, 20))
        campos_der.columnconfigure(1, weight=1)

        card_form.columnconfigure(0, weight=1)
        card_form.columnconfigure(1, weight=1)

        self.entry_id = self.crear_entry(campos_izq, "ID Médico:", 0)
        self.entry_nombre = self.crear_entry(campos_izq, "Nombre:", 1)
        self.entry_telefono = self.crear_entry(campos_izq, "Teléfono:", 2)
        self.entry_genero = self.crear_entry(campos_der, "Género:", 0)
        self.entry_especialidad = self.crear_entry(campos_der, "Especialidad:", 1)

        self._entries = [self.entry_id, self.entry_nombre, self.entry_telefono,
                         self.entry_genero, self.entry_especialidad]

        # Botones de acción
        frame_btns = ctk.CTkFrame(card_form, fg_color="transparent")
        frame_btns.grid(row=2, column=0, columnspan=4, pady=(20, 20), padx=20, sticky="w")

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

        # --- Tabla ---
        columnas = ("ID", "Nombre", "Teléfono", "Género", "Especialidad")
        anchos = (70, 180, 120, 100, 180)
        self.tree = self.crear_treeview(self.scroll_frame, columnas, anchos)

        # --- Botón Exportar ---
        frame_export = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        frame_export.pack(fill="x", padx=30, pady=(0, 30))
        self.crear_boton(
            frame_export, "📥 Exportar a Excel", 
            lambda: self.exportar_excel(self.tree, "reporte_medicos"),
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
        id_m = self.entry_id.get().strip()
        nombre = self.entry_nombre.get().strip()
        telefono = self.entry_telefono.get().strip()
        genero = self.entry_genero.get().strip()
        especialidad = self.entry_especialidad.get().strip()

        if not id_m or not nombre:
            messagebox.showwarning("Campos vacíos",
                                   "ID y Nombre son obligatorios.", parent=self.app)
            return
        try:
            id_m = int(id_m)
        except ValueError:
            messagebox.showerror("Error de formato",
                                 "ID debe ser un número entero.", parent=self.app)
            return

        ok = self.controller.registrar(id_m, nombre, telefono, genero, especialidad)
        if ok:
            messagebox.showinfo("Éxito", "✅ Médico registrado correctamente.",
                                parent=self.app)
            self._limpiar_campos()
            self._refrescar()
        else:
            messagebox.showerror("Error",
                                 "No se pudo registrar. Verifique que el ID no esté duplicado.",
                                 parent=self.app)

    def _cargar_seleccion(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selección",
                                   "Seleccione un médico de la tabla.", parent=self.app)
            return
        valores = self.tree.item(sel[0], "values")
        self._limpiar_campos()
        self.entry_id.insert(0, valores[0])
        self.bloquear_entry(self.entry_id)
        self.entry_nombre.insert(0, valores[1])
        self.entry_telefono.insert(0, valores[2])
        self.entry_genero.insert(0, valores[3])
        self.entry_especialidad.insert(0, valores[4])

    def _guardar_cambios(self):
        id_m = self.entry_id.get().strip()
        nombre = self.entry_nombre.get().strip()
        telefono = self.entry_telefono.get().strip()
        genero = self.entry_genero.get().strip()
        especialidad = self.entry_especialidad.get().strip()

        if not id_m or not nombre:
            messagebox.showwarning("Campos vacíos",
                                   "ID y Nombre son obligatorios.", parent=self.app)
            return
        try:
            id_m = int(id_m)
        except ValueError:
            messagebox.showerror("Error de formato",
                                 "ID debe ser un número entero.", parent=self.app)
            return

        ok = self.controller.actualizar(id_m, nombre, telefono, genero, especialidad)
        if ok:
            messagebox.showinfo("Éxito", "✅ Médico actualizado.", parent=self.app)
            self._limpiar_campos()
            self._refrescar()
        else:
            messagebox.showerror("Error", "No se pudo actualizar.", parent=self.app)

    def _eliminar(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selección",
                                   "Seleccione un médico de la tabla.", parent=self.app)
            return
        valores = self.tree.item(sel[0], "values")
        id_m = valores[0]
        confirm = messagebox.askyesno("Confirmar",
                                      f"¿Eliminar médico ID {id_m} - {valores[1]}?",
                                      parent=self.app)
        if confirm:
            ok = self.controller.eliminar(id_m)
            if ok:
                messagebox.showinfo("Éxito", "Médico eliminado.", parent=self.app)
                self._refrescar()
            else:
                messagebox.showerror("Error",
                                     "No se pudo eliminar. Puede tener citas o "
                                     "enfermeras asociadas.", parent=self.app)
