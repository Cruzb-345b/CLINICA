"""
controllers/medicos_controller.py
Lógica de negocio CRUD para la tabla MEDICO.
"""


class MedicosController:
    """Controlador del módulo Médicos."""

    def __init__(self, db):
        self.db = db

    def listar(self):
        """Retorna todos los médicos ordenados por ID."""
        return self.db.ejecutar_lectura("SELECT * FROM MEDICO ORDER BY ID_MEDICO")

    def buscar(self, termino):
        """Busca médicos por ID o Nombre."""
        query = "SELECT * FROM MEDICO WHERE CAST(ID_MEDICO AS CHAR) LIKE %s OR NOMBRE LIKE %s ORDER BY ID_MEDICO"
        like_term = f"%{termino}%"
        return self.db.ejecutar_lectura(query, (like_term, like_term))

    def registrar(self, id_medico, nombre, telefono, genero, especialidad):
        """
        Inserta un nuevo médico.
        Retorna True si fue exitoso, False en caso contrario.
        """
        return self.db.ejecutar_consulta(
            "INSERT INTO MEDICO (ID_MEDICO, NOMBRE, TELEFONO, GENERO, ESPECIALIDAD) "
            "VALUES (%s, %s, %s, %s, %s)",
            (id_medico, nombre, telefono, genero, especialidad),
        )

    def actualizar(self, id_medico, nombre, telefono, genero, especialidad):
        """
        Actualiza un médico existente.
        Retorna True si fue exitoso, False en caso contrario.
        """
        return self.db.ejecutar_consulta(
            "UPDATE MEDICO SET NOMBRE=%s, TELEFONO=%s, GENERO=%s, ESPECIALIDAD=%s "
            "WHERE ID_MEDICO=%s",
            (nombre, telefono, genero, especialidad, id_medico),
        )

    def eliminar(self, id_medico):
        """
        Elimina un médico por ID.
        Retorna True si fue exitoso, False en caso contrario.
        """
        return self.db.ejecutar_consulta(
            "DELETE FROM MEDICO WHERE ID_MEDICO = %s",
            (id_medico,),
        )
