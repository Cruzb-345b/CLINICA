"""
controllers/login_controller.py
Controlador para el inicio de sesión.
"""

class LoginController:
    def __init__(self, db):
        self.db = db
        
    def autenticar(self, username, password):
        """Verifica si las credenciales son correctas y retorna (True, Rol) o (False, None)."""
        query = "SELECT ROL FROM USUARIOS WHERE USERNAME = %s AND PASSWORD = %s LIMIT 1"
        resultado = self.db.ejecutar_lectura(query, (username, password))
        
        if resultado and len(resultado) > 0:
            return True, resultado[0][0]
        return False, None
