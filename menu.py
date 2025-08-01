# menu.py
import pygame
from settings_menu import SettingsMenu
from difficulty_menu import DifficultyMenu
from ui_theme import *

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(FONT_PATH, FONT_SIZE)
        self.settings_menu = SettingsMenu(screen)
        self.difficulty_menu = DifficultyMenu(screen)

        self.buttons = ["Jouer", "Options", "Quitter"]
        self.selected_index = 0

    def draw_colored_title(self):
        """Dessine le titre avec les 4 couleurs alternées sur chaque lettre (ignorant les espaces)"""
        title = "Le jeu du puzzle"
        title_font = get_title_font()  # Utiliser la nouvelle police de titre
        
        # Position de départ pour centrer le titre
        total_width = 0
        letter_surfaces = []
        color_index = 0  # Index séparé pour les couleurs (n'augmente pas pour les espaces)
        
        # Préparer chaque lettre avec sa couleur
        for letter in title:
            if letter == ' ':
                # Pour les espaces, créer une surface avec la couleur de fond (invisible)
                letter_surface = title_font.render(' ', True, COLOR_TEXT)
                # Ne pas incrémenter color_index pour les espaces
            else:
                # Utiliser les couleurs des boutons en alternance (seulement pour les lettres)
                color = BUTTON_COLORS[color_index % len(BUTTON_COLORS)]
                letter_surface = title_font.render(letter, True, color)
                color_index += 1  # Incrémenter seulement pour les lettres
            
            letter_surfaces.append(letter_surface)
            total_width += letter_surface.get_width()
        
        # Position de départ pour centrer horizontalement
        start_x = (self.screen.get_width() - total_width) // 2
        y_pos = 60  # Position verticale du titre (un peu plus haut pour la police plus grande)
        
        # Dessiner chaque lettre
        current_x = start_x
        for letter_surface in letter_surfaces:
            self.screen.blit(letter_surface, (current_x, y_pos))
            current_x += letter_surface.get_width()

    def draw(self):
        self.screen.fill(COLOR_BG)
        
        # Dessiner le logo en bas à gauche
        draw_logo(self.screen, "bottom-left")
        
        # Dessiner le titre coloré "Le jeu du puzzle"
        self.draw_colored_title()
        
        for index, button in enumerate(self.buttons):
            # Utiliser la couleur spécifique du bouton si survolé
            is_hovered = (index == self.selected_index)
            text = self.font.render(button, True, COLOR_TEXT)
            rect = text.get_rect(center=(self.screen.get_width() // 2, 280 + index * 60))  # Décalé encore plus pour la police plus grande
            
            # Dessiner un rectangle coloré derrière le texte si survolé
            if is_hovered:
                button_rect = pygame.Rect(rect.left - 20, rect.top - 10, rect.width + 40, rect.height + 20)
                pygame.draw.rect(self.screen, get_button_color(index, True), button_rect, border_radius=10)
            
            self.screen.blit(text, rect)

    def run(self):
        while True:
            self.draw()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit", None
                elif event.type == pygame.MOUSEMOTION:
                    self.update_selection_with_mouse(event.pos)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        return self.get_action()

            self.clock.tick(60)

    def update_selection_with_mouse(self, mouse_pos):
        old_selection = self.selected_index
        self.selected_index = -1  # Aucune sélection par défaut
        
        for index, button in enumerate(self.buttons):
            text = self.font.render(button, True, COLOR_TEXT)
            rect = text.get_rect(center=(self.screen.get_width() // 2, 280 + index * 60))
            # Zone de clic élargie pour une meilleure détection
            expanded_rect = pygame.Rect(rect.left - 50, rect.top - 20, rect.width + 100, rect.height + 40)
            if expanded_rect.collidepoint(mouse_pos):
                self.selected_index = index
                break

    def get_action(self):
        if self.selected_index >= 0:  # Seulement si quelque chose est sélectionné
            if self.selected_index == 0:  # Jouer
                return self.difficulty_menu.run()
            elif self.selected_index == 1:  # Options
                self.settings_menu.run()
                return None, None
            elif self.selected_index == 2:  # Quitter
                return "quit", None
        return None, None