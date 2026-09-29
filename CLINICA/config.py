"""
config.py - Configuración global del Sistema de Gestión Clínica
Contiene colores, fuentes, rutas de assets y utilidades de imagen.
"""

import os
from dotenv import load_dotenv

# ============================================================
#  RUTAS DE ASSETS Y ENTORNO
# ============================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

load_dotenv(os.path.join(BASE_DIR, ".env"))

try:
    import customtkinter as ctk
    from PIL import Image, ImageDraw
    PIL_DISPONIBLE = True
except ImportError:
    PIL_DISPONIBLE = False

LOGO_PATH = os.path.join(ASSETS_DIR, "logo_clinica.jpg")
BANNER_PATH = os.path.join(ASSETS_DIR, "banner_dashboard.jpg")
ICONOS_PATH = os.path.join(ASSETS_DIR, "iconos_modulos.jpg")


# ============================================================
#  PALETA DE COLORES (Minimalista / CTK)
# ============================================================
COLOR_BG = "#1e1e1e"           # Fondo principal
COLOR_SIDEBAR = "#2b2b2b"      # Panel lateral
COLOR_CARD = "#252526"         # Tarjetas
COLOR_PRIMARY = "#1f6aa5"      # Azul moderno de CTK
COLOR_PRIMARY_HOVER = "#144870"
COLOR_SUCCESS = "#22c55e"      
COLOR_DANGER = "#ef4444"       
COLOR_WARNING = "#f59e0b"      
COLOR_PURPLE = "#a855f7"       
COLOR_TEXT = "#ffffff"         
COLOR_TEXT_SEC = "#a1a1aa"     
COLOR_TABLE_BG = "#2b2b2b"
COLOR_TABLE_FG = "#ffffff"
COLOR_TABLE_SEL = "#1f6aa5"
COLOR_TABLE_STRIPE = "#333333"
COLOR_ENTRY_BORDER = "#3a3a3a"
COLOR_ENTRY_BG = "#1a1a1a"

# ============================================================
#  FUENTES
# ============================================================
FONT_TITLE = ("Roboto", 22, "bold")
FONT_SUBTITLE = ("Roboto", 16, "bold")
FONT_BODY = ("Roboto", 12)
FONT_SMALL = ("Roboto", 10)
FONT_BUTTON = ("Roboto", 13, "bold")
FONT_ICON = ("Roboto", 24)
FONT_HERO = ("Roboto", 26, "bold")
FONT_HERO_SUB = ("Roboto", 14)


# ============================================================
#  UTILIDADES DE IMAGEN (Adaptado a CTkImage)
# ============================================================
def cargar_imagen(path, size):
    if not PIL_DISPONIBLE or not os.path.exists(path): return None
    try:
        img = Image.open(path)
        return ctk.CTkImage(light_image=img, dark_image=img, size=size)
    except Exception: return None

def crear_imagen_circular(path, diametro):
    if not PIL_DISPONIBLE or not os.path.exists(path): return None
    try:
        img = Image.open(path).resize((diametro, diametro), Image.LANCZOS)
        mask_size = (diametro * 4, diametro * 4)
        mask = Image.new("L", mask_size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, mask_size[0], mask_size[1]), fill=255)
        mask = mask.resize((diametro, diametro), Image.LANCZOS)
        resultado = Image.new("RGBA", (diametro, diametro), (0, 0, 0, 0))
        resultado.paste(img, (0, 0))
        resultado.putalpha(mask)
        return ctk.CTkImage(light_image=resultado, dark_image=resultado, size=(diametro, diametro))
    except Exception: return None

def recortar_icono(path, cuadrante, size):
    if not PIL_DISPONIBLE or not os.path.exists(path): return None
    try:
        img = Image.open(path)
        w, h = img.size
        mitad_w, mitad_h = w // 2, h // 2
        cajas = [
            (0, 0, mitad_w, mitad_h),
            (mitad_w, 0, w, mitad_h),
            (0, mitad_h, mitad_w, h),
            (mitad_w, mitad_h, w, h),
        ]
        icono = img.crop(cajas[cuadrante])
        return ctk.CTkImage(light_image=icono, dark_image=icono, size=size)
    except Exception: return None
