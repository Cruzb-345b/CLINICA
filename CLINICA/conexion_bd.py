"""
conexion_bd.py - Módulo de conexión a la base de datos MySQL
Sistema de Gestión Clínica
"""

import mysql.connector
from mysql.connector import Error


class ConexionBD:
    """Clase para gestionar la conexión y operaciones con MySQL."""

    def __init__(self, host="localhost", user="root", password="", database="clinica"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conexion = None

    def conectar(self):
        """Establece la conexión con el servidor MySQL."""
        try:
            self.conexion = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.conexion.is_connected():
                return True
        except Error as e:
            print(f"[ERROR] No se pudo conectar a MySQL: {e}")
            return False

    def desconectar(self):
        """Cierra la conexión activa."""
        if self.conexion and self.conexion.is_connected():
            self.conexion.close()

    def ejecutar_consulta(self, query, valores=None):
        """
        Ejecuta INSERT, UPDATE o DELETE.
        Retorna True si fue exitoso, False en caso contrario.
        """
        try:
            if not self.conectar():
                return False
            cursor = self.conexion.cursor()
            cursor.execute(query, valores)
            self.conexion.commit()
            return True
        except Error as e:
            print(f"[ERROR] al ejecutar consulta: {e}")
            return False
        finally:
            self.desconectar()

    def ejecutar_lectura(self, query, valores=None):
        """
        Ejecuta SELECT y retorna una lista de tuplas con los resultados.
        Retorna lista vacía si hay error.
        """
        try:
            if not self.conectar():
                return []
            cursor = self.conexion.cursor()
            cursor.execute(query, valores)
            resultados = cursor.fetchall()
            return resultados
        except Error as e:
            print(f"[ERROR] al ejecutar lectura: {e}")
            return []
        finally:
            self.desconectar()

    def existe_registro(self, tabla, campo_id, valor_id):
        """
        Verifica si un registro existe en una tabla dada.
        Retorna True si existe, False si no.
        """
        query = f"SELECT 1 FROM {tabla} WHERE {campo_id} = %s LIMIT 1"
        resultado = self.ejecutar_lectura(query, (valor_id,))
        return len(resultado) > 0
