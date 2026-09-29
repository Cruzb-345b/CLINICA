"""
controllers/pacientes_controller.py
Lógica de negocio CRUD para la tabla PACIENTE.
"""


class PacientesController:
    """Controlador del módulo Pacientes."""

    def __init__(self, db):
        self.db = db

    def listar(self):
        """Retorna todos los pacientes ordenados por ID."""
        return self.db.ejecutar_lectura("SELECT * FROM PACIENTE ORDER BY ID_PACIENTE")

    def buscar(self, termino):
        """Busca pacientes por ID o Nombre."""
        query = "SELECT * FROM PACIENTE WHERE CAST(ID_PACIENTE AS CHAR) LIKE %s OR NOMBRE LIKE %s ORDER BY ID_PACIENTE"
        like_term = f"%{termino}%"
        return self.db.ejecutar_lectura(query, (like_term, like_term))

    def registrar(self, id_paciente, nombre, edad):
        """
        Inserta un nuevo paciente.
        Retorna True si fue exitoso, False en caso contrario.
        """
        return self.db.ejecutar_consulta(
            "INSERT INTO PACIENTE (ID_PACIENTE, NOMBRE, EDAD) VALUES (%s, %s, %s)",
            (id_paciente, nombre, edad),
        )

    def actualizar(self, id_paciente, nombre, edad):
        """
        Actualiza un paciente existente.
        Retorna True si fue exitoso, False en caso contrario.
        """
        return self.db.ejecutar_consulta(
            "UPDATE PACIENTE SET NOMBRE = %s, EDAD = %s WHERE ID_PACIENTE = %s",
            (nombre, edad, id_paciente),
        )

    def eliminar(self, id_paciente):
        """
        Elimina un paciente por ID.
        Retorna True si fue exitoso, False en caso contrario.
        """
        return self.db.ejecutar_consulta(
            "DELETE FROM PACIENTE WHERE ID_PACIENTE = %s",
            (id_paciente,),
        )
