# 🏥 Sistema de Gestión Clínica

Una aplicación de escritorio moderna y escalable desarrollada en Python para la administración de centros médicos. Este sistema cuenta con una arquitectura de software modular (MVC), interfaz gráfica minimalista (Dark Mode) y conexión a una base de datos relacional MySQL.

## ✨ Características Principales

- 🔒 **Sistema de Autenticación (Gatekeeper):** Acceso restringido mediante credenciales seguras.
- 📊 **Dashboard Analítico:** Visualización de datos en tiempo real con gráficos interactivos (Matplotlib).
- 👥 **Gestión de Pacientes y Médicos:** Módulos CRUD completos (Crear, Leer, Actualizar, Eliminar) con barra de búsqueda dinámica.
- 📅 **Gestión de Citas:** Asignación de citas médicas con validación de llaves foráneas.
- 📥 **Generación de Reportes:** 
  - Exportación de tablas masivas a **Excel** (Pandas).
  - Generación de tickets/recetas individuales en **PDF** (FPDF).
- 🎨 **Diseño UX/UI Moderno:** Interfaz construida con CustomTkinter aplicando principios minimalistas.
- 🛡️ **Seguridad:** Protección de credenciales de base de datos mediante variables de entorno (`.env`).

## 🛠️ Tecnologías y Librerías Utilizadas

- **Lenguaje:** Python 3.x
- **Base de Datos:** MySQL
- **Interfaz Gráfica:** CustomTkinter (CTK)
- **Visualización de Datos:** Matplotlib
- **Procesamiento de Datos:** Pandas, Openpyxl
- **Generación de Documentos:** FPDF
- **Seguridad y Entorno:** python-dotenv, mysql-connector-python

## 📂 Estructura del Proyecto

```text
CLINICA/
├── assets/                 # Imágenes, iconos y logotipos
├── BD/
│   └── script_clinica.sql  # Script de creación de la base de datos
├── controllers/            # Lógica de negocio y consultas SQL
├── database/
│   └── conexion.py         # Manejador de la conexión a MySQL
├── views/                  # Interfaces gráficas de cada módulo
├── .env.example            # Plantilla de variables de entorno
├── config.py               # Configuraciones globales de diseño y rutas
├── main.py                 # Punto de entrada de la aplicación
└── README.md
