# ui_theme.py
import pygame
import os

# Couleurs
COLOR_BG = (30, 30, 30)  # gris très foncé
COLOR_BTN = (60, 120, 200)  # bleu sobre
COLOR_BTN_HOVER = (90, 150, 240)
COLOR_TEXT = (255, 255, 255)  # blanc
COLOR_SELECTED = (100, 149, 237)

# Couleurs spécifiques pour chaque bouton (hover/selection)
BUTTON_COLORS = [
    (220, 60, 60),   # Rouge pour le 1er bouton
    (60, 60, 150),   # Bleu foncé pour le 2ème bouton
    (220, 200, 60),  # Jaune pour le 3ème bouton
    (100, 180, 220)  # Bleu clair pour le 4ème bouton
]

# Couleurs pour les difficultés (même ordre)
DIFFICULTY_COLORS = {
    "Facile": (220, 60, 60),      # Rouge
    "Moyen": (60, 60, 150),       # Bleu foncé
    "Difficile": (220, 200, 60),  # Jaune
    "Impossible": (100, 180, 220) # Bleu clair
}

# Boutons
BUTTON_WIDTH = 250
BUTTON_HEIGHT = 60
BUTTON_RADIUS = 12  # coins arrondis

# Polices
FONT_PATH = None  # ou "assets/fonts/Roboto-Regular.ttf"
FONT_SIZE = 32
TITLE_FONT_SIZE = 64  # Plus grande taille pour les titres

# Logo
_logo_cache = None

def get_title_font():
    """Retourne la police pour les titres"""
    return pygame.font.Font(None, TITLE_FONT_SIZE)  # Police système par défaut, plus grande

def get_button_color(index, selected=False):
    """Retourne la couleur appropriée pour un bouton selon son index"""
    if selected and index < len(BUTTON_COLORS):
        return BUTTON_COLORS[index]
    return COLOR_BTN

def get_difficulty_color(difficulty_name):
    """Retourne la couleur associée à une difficulté"""
    return DIFFICULTY_COLORS.get(difficulty_name, COLOR_SELECTED)

def load_logo():
    """Charge le logo du jeu"""
    global _logo_cache
    if _logo_cache is None:
        try:
            if os.path.exists("assets/puzzle.webp"):
                logo = pygame.image.load("assets/puzzle.webp")
                # Redimensionner le logo à une taille plus grande (120x120 pixels)
                _logo_cache = pygame.transform.scale(logo, (120, 120))
            else:
                # Logo par défaut si l'image n'existe pas
                _logo_cache = pygame.Surface((120, 120))
                _logo_cache.fill((100, 149, 237))
        except:
            # Logo par défaut en cas d'erreur
            _logo_cache = pygame.Surface((120, 120))
            _logo_cache.fill((100, 149, 237))
    return _logo_cache

def draw_logo(screen, position="top-right"):
    """Dessine le logo à la position spécifiée
    Positions possibles: top-left, top-right, bottom-left, bottom-right"""
    logo = load_logo()
    
    if position == "top-right":
        x = screen.get_width() - logo.get_width() - 20
        y = 20
    elif position == "top-left":
        x = 20
        y = 20
    elif position == "bottom-right":
        x = screen.get_width() - logo.get_width() - 20
        y = screen.get_height() - logo.get_height() - 20
    elif position == "bottom-left":
        x = 20
        y = screen.get_height() - logo.get_height() - 20
    else:
        x, y = 20, 20  # Par défaut en haut à gauche
    
    screen.blit(logo, (x, y))
