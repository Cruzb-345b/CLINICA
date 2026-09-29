"""
views/login_view.py
Pantalla de inicio de sesión (Gatekeeper).
"""

import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from config import COLOR_BG, COLOR_CARD, COLOR_TEXT, COLOR_TEXT_SEC, COLOR_ENTRY_BG, COLOR_ENTRY_BORDER, COLOR_PRIMARY, COLOR_PRIMARY_HOVER, FONT_TITLE, FONT_BODY, FONT_BUTTON
from controllers.login_controller import LoginController

class LoginView:
    """Pantalla de Login que bloquea el acceso principal."""
    def __init__(self, parent, app, on_success):
        self.parent = parent
        self.app = app
        self.on_success = on_success
        self.controller = LoginController(app.db)
        
        self.frame = ctk.CTkFrame(self.parent, fg_color=COLOR_BG, corner_radius=0)
        self.frame.pack(fill="both", expand=True)
        
        self._construir()
        
    def _construir(self):
        # Contenedor centrado
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(2, weight=1)
        
        card = ctk.CTkFrame(self.frame, fg_color=COLOR_CARD, corner_radius=15, border_width=1, border_color=COLOR_ENTRY_BORDER)
        card.grid(row=1, column=1, padx=40, pady=40, ipadx=20, ipady=20)
        
        # Logo o Ícono
        if self.app.imagenes.get("logo"):
            ctk.CTkLabel(card, image=self.app.imagenes["logo"], text="").pack(pady=(20, 16))
            
        ctk.CTkLabel(card, text="Iniciar Sesión", font=FONT_TITLE, text_color=COLOR_TEXT).pack(pady=(0, 24))
        
        # Usuario
        ctk.CTkLabel(card, text="Usuario:", font=FONT_BODY, text_color=COLOR_TEXT_SEC, anchor="w").pack(fill="x", padx=30)
        self.entry_user = ctk.CTkEntry(card, font=FONT_BODY, fg_color=COLOR_ENTRY_BG, text_color=COLOR_TEXT, border_color=COLOR_ENTRY_BORDER, corner_radius=8, width=250)
        self.entry_user.pack(fill="x", ipady=6, pady=(4, 16), padx=30)
        self.entry_user.focus()
        
        # Contraseña
        ctk.CTkLabel(card, text="Contraseña:", font=FONT_BODY, text_color=COLOR_TEXT_SEC, anchor="w").pack(fill="x", padx=30)
        self.entry_pass = ctk.CTkEntry(card, show="*", font=FONT_BODY, fg_color=COLOR_ENTRY_BG, text_color=COLOR_TEXT, border_color=COLOR_ENTRY_BORDER, corner_radius=8, width=250)
        self.entry_pass.pack(fill="x", ipady=6, pady=(4, 24), padx=30)
        self.entry_pass.bind("<Return>", lambda e: self._login())
        
        # Botón
        btn = ctk.CTkButton(card, text="Acceder", font=FONT_BUTTON, fg_color=COLOR_PRIMARY, hover_color=COLOR_PRIMARY_HOVER, text_color="white", corner_radius=8, command=self._login)
        btn.pack(fill="x", ipady=6, padx=30, pady=(0, 20))
        
    def _login(self):
        user = self.entry_user.get().strip()
        pwd = self.entry_pass.get().strip()
        
        if not user or not pwd:
            messagebox.showwarning("Error", "Ingrese usuario y contraseña.")
            return
            
        ok, rol = self.controller.autenticar(user, pwd)
        if ok:
            self.frame.destroy()
            self.on_success(user, rol)
        else:
            messagebox.showerror("Error", "Credenciales incorrectas.")
            self.entry_pass.delete(0, tk.END)
