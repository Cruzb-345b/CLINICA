"""Paquete views - Capa de presentación (interfaz gráfica)."""
from .base_view import BaseView
from .dashboard_view import DashboardView
from .pacientes_view import PacientesView
from .medicos_view import MedicosView
from .citas_view import CitasView

__all__ = [
    "BaseView",
    "DashboardView",
    "PacientesView",
    "MedicosView",
    "CitasView",
]
