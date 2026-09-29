"""
controllers/dashboard_controller.py
Lógica de negocio para el Dashboard: conteos y últimas citas.
"""


class DashboardController:
    """Controlador del módulo Dashboard."""

    def __init__(self, db):
        self.db = db

    def obtener_conteo_pacientes(self):
        """Retorna el número total de pacientes."""
        resultado = self.db.ejecutar_lectura("SELECT COUNT(*) FROM PACIENTE")
        return resultado[0][0] if resultado else "—"

    def obtener_conteo_medicos(self):
        """Retorna el número total de médicos."""
        resultado = self.db.ejecutar_lectura("SELECT COUNT(*) FROM MEDICO")
        return resultado[0][0] if resultado else "—"

    def obtener_conteo_citas(self):
        """Retorna el número total de citas."""
        resultado = self.db.ejecutar_lectura("SELECT COUNT(*) FROM CITA")
        return resultado[0][0] if resultado else "—"

    def obtener_conteo_enfermeras(self):
        """Retorna el número total de enfermeras."""
        resultado = self.db.ejecutar_lectura("SELECT COUNT(*) FROM ENFERMERA")
        return resultado[0][0] if resultado else "—"

    def obtener_ultimas_citas(self, limite=10):
        """Retorna las últimas citas con nombres de médico y paciente."""
        query = """
            SELECT c.ID_CITA, m.NOMBRE, p.NOMBRE, c.ID_CONSULTORIO, c.FECHA, c.HORA
            FROM CITA c
            LEFT JOIN MEDICO m ON c.ID_MEDICO = m.ID_MEDICO
            LEFT JOIN PACIENTE p ON c.ID_PACIENTE = p.ID_PACIENTE
            ORDER BY c.ID_CITA DESC
            LIMIT %s
        """
        return self.db.ejecutar_lectura(query, (limite,))

    def obtener_citas_por_medico(self):
        """Retorna datos para el gráfico de barras: citas agrupadas por médico."""
        query = """
            SELECT m.NOMBRE, COUNT(c.ID_CITA)
            FROM MEDICO m
            LEFT JOIN CITA c ON m.ID_MEDICO = c.ID_MEDICO
            GROUP BY m.ID_MEDICO, m.NOMBRE
            ORDER BY COUNT(c.ID_CITA) DESC
            LIMIT 5
        """
        return self.db.ejecutar_lectura(query)

    def obtener_medicos_por_especialidad(self):
        """Retorna datos para el gráfico de torta: distribución de especialidades."""
        query = """
            SELECT ESPECIALIDAD, COUNT(*)
            FROM MEDICO
            GROUP BY ESPECIALIDAD
        """
        return self.db.ejecutar_lectura(query)
