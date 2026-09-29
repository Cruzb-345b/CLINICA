"""Paquete controllers - Capa de lógica de negocio."""
from .dashboard_controller import DashboardController
from .pacientes_controller import PacientesController
from .medicos_controller import MedicosController
from .citas_controller import CitasController

__all__ = [
    "DashboardController",
    "PacientesController",
    "MedicosController",
    "CitasController",
]
