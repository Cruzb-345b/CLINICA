"""
controllers/citas_controller.py
Lógica de negocio para la tabla CITA, incluyendo validaciones de FK.
"""


class CitasController:
    """Controlador del módulo Citas."""

    def __init__(self, db):
        self.db = db

    def listar(self):
        """Retorna todas las citas con nombres de médico y paciente."""
        query = """
            SELECT c.ID_CITA, m.NOMBRE, p.NOMBRE, c.ID_CONSULTORIO, c.FECHA, c.HORA
            FROM CITA c
            LEFT JOIN MEDICO m ON c.ID_MEDICO = m.ID_MEDICO
            LEFT JOIN PACIENTE p ON c.ID_PACIENTE = p.ID_PACIENTE
            ORDER BY c.ID_CITA DESC
        """
        return self.db.ejecutar_lectura(query)

    def buscar(self, termino):
        """Busca citas por ID de cita, nombre de médico o nombre de paciente."""
        query = """
            SELECT c.ID_CITA, m.NOMBRE, p.NOMBRE, c.ID_CONSULTORIO, c.FECHA, c.HORA
            FROM CITA c
            LEFT JOIN MEDICO m ON c.ID_MEDICO = m.ID_MEDICO
            LEFT JOIN PACIENTE p ON c.ID_PACIENTE = p.ID_PACIENTE
            WHERE CAST(c.ID_CITA AS CHAR) LIKE %s 
               OR m.NOMBRE LIKE %s 
               OR p.NOMBRE LIKE %s
            ORDER BY c.ID_CITA DESC
        """
        like_term = f"%{termino}%"
        return self.db.ejecutar_lectura(query, (like_term, like_term, like_term))

    def existe_medico(self, id_medico):
        """Verifica si un médico existe en la BD."""
        return self.db.existe_registro("MEDICO", "ID_MEDICO", id_medico)

    def existe_paciente(self, id_paciente):
        """Verifica si un paciente existe en la BD."""
        return self.db.existe_registro("PACIENTE", "ID_PACIENTE", id_paciente)

    def asegurar_consultorio(self, id_consultorio):
        """Crea el consultorio si no existe."""
        if not self.db.existe_registro("CONSULTORIO", "ID_CONSULTORIO", id_consultorio):
            self.db.ejecutar_consulta(
                "INSERT INTO CONSULTORIO (ID_CONSULTORIO) VALUES (%s)",
                (id_consultorio,),
            )

    def registrar(self, id_cita, id_medico, id_paciente, id_consultorio, fecha, hora):
        """
        Registra una nueva cita.
        Retorna un dict con 'ok' (bool) y 'error' (str o None).
        Valida que médico y paciente existan antes de insertar.
        """
        # Validar médico
        if not self.existe_medico(id_medico):
            return {
                "ok": False,
                "error": f"No existe un médico con ID {id_medico}.\n"
                         f"Registre al médico primero en el módulo Médicos.",
                "tipo": "medico_no_encontrado",
            }

        # Validar paciente
        if not self.existe_paciente(id_paciente):
            return {
                "ok": False,
                "error": f"No existe un paciente con ID {id_paciente}.\n"
                         f"Registre al paciente primero en el módulo Pacientes.",
                "tipo": "paciente_no_encontrado",
            }

        # Asegurar consultorio
        self.asegurar_consultorio(id_consultorio)

        # Insertar cita
        ok = self.db.ejecutar_consulta(
            "INSERT INTO CITA (ID_CITA, ID_MEDICO, ID_PACIENTE, ID_CONSULTORIO, FECHA, HORA) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (id_cita, id_medico, id_paciente, id_consultorio, fecha, hora),
        )

        if ok:
            return {"ok": True, "error": None, "tipo": None}
        else:
            return {
                "ok": False,
                "error": "No se pudo registrar la cita. Verifique los datos y el formato de fecha/hora.",
                "tipo": "error_insercion",
            }

    def eliminar(self, id_cita):
        """
        Elimina una cita por ID.
        Retorna True si fue exitoso, False en caso contrario.
        """
        return self.db.ejecutar_consulta(
            "DELETE FROM CITA WHERE ID_CITA = %s",
            (id_cita,),
        )

    def generar_ticket_pdf(self, id_cita):
        """Genera un ticket en PDF para una cita específica."""
        query = """
            SELECT c.ID_CITA, m.NOMBRE, p.NOMBRE, c.ID_CONSULTORIO, c.FECHA, c.HORA
            FROM CITA c
            LEFT JOIN MEDICO m ON c.ID_MEDICO = m.ID_MEDICO
            LEFT JOIN PACIENTE p ON c.ID_PACIENTE = p.ID_PACIENTE
            WHERE c.ID_CITA = %s
        """
        resultado = self.db.ejecutar_lectura(query, (id_cita,))
        if not resultado:
            return False, "Cita no encontrada."
            
        datos = resultado[0]
        
        try:
            from fpdf import FPDF
            import os
            
            pdf = FPDF()
            pdf.add_page()
            
            # Título
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(190, 10, txt="SISTEMA DE GESTIÓN CLÍNICA", ln=True, align='C')
            pdf.set_font("Arial", 'I', 12)
            pdf.cell(190, 10, txt="Ticket de Cita Médica", ln=True, align='C')
            pdf.ln(10)
            
            # Detalles
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(50, 10, txt="ID Cita:", ln=False)
            pdf.set_font("Arial", '', 12)
            pdf.cell(140, 10, txt=str(datos[0]), ln=True)
            
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(50, 10, txt="Médico:", ln=False)
            pdf.set_font("Arial", '', 12)
            pdf.cell(140, 10, txt=str(datos[1]), ln=True)
            
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(50, 10, txt="Paciente:", ln=False)
            pdf.set_font("Arial", '', 12)
            pdf.cell(140, 10, txt=str(datos[2]), ln=True)
            
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(50, 10, txt="Consultorio:", ln=False)
            pdf.set_font("Arial", '', 12)
            pdf.cell(140, 10, txt=str(datos[3]), ln=True)
            
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(50, 10, txt="Fecha:", ln=False)
            pdf.set_font("Arial", '', 12)
            pdf.cell(140, 10, txt=str(datos[4]), ln=True)
            
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(50, 10, txt="Hora:", ln=False)
            pdf.set_font("Arial", '', 12)
            pdf.cell(140, 10, txt=str(datos[5]), ln=True)
            
            pdf.ln(20)
            pdf.set_font("Arial", 'I', 10)
            pdf.cell(190, 10, txt="Por favor, presentese 15 minutos antes de su cita.", ln=True, align='C')
            
            # Guardar en raíz
            nombre_archivo = f"ticket_cita_{datos[0]}.pdf"
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            ruta = os.path.join(base_dir, nombre_archivo)
            
            pdf.output(ruta)
            return True, ruta
        except Exception as e:
            return False, str(e)
