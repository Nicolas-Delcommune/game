# pause_menu.py
import pygame
from settings_menu import SettingsMenu
from ui_theme import *

class PauseMenu:
    def __init__(self, screen, background_surface=None):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(FONT_PATH, FONT_SIZE)
        self.running = True
        self.background_surface = background_surface
        self.buttons = [
            {"label": "Retour au jeu", "action": "resume"},
            {"label": "Paramètres", "action": "settings"},
            {"label": "Abandonner", "action": "abandon"},
            {"label": "Menu principal", "action": "menu"}
        ]
        self.hovered_index = None

    def draw_button(self, text, rect, hovered, index):
        # Utiliser la couleur spécifique du bouton si survolé
        color = get_button_color(index, hovered) if hovered else COLOR_BTN
        pygame.draw.rect(self.screen, color, rect, border_radius=BUTTON_RADIUS)
        txt_surface = self.font.render(text, True, COLOR_TEXT)
        txt_rect = txt_surface.get_rect(center=rect.center)
        self.screen.blit(txt_surface, txt_rect)

    def create_blurred_background(self):
        """Créer un arrière-plan flouté du plateau de jeu"""
        if self.background_surface:
            # Créer une copie de la surface de fond
            blurred = self.background_surface.copy()
            
            # Appliquer un effet de flou simple en réduisant puis agrandissant l'image
            # Et en appliquant une couche semi-transparente
            small_size = (blurred.get_width() // 8, blurred.get_height() // 8)
            blurred = pygame.transform.scale(blurred, small_size)
            blurred = pygame.transform.scale(blurred, (self.background_surface.get_width(), self.background_surface.get_height()))
            
            # Ajouter une couche semi-transparente sombre
            overlay = pygame.Surface((blurred.get_width(), blurred.get_height()))
            overlay.set_alpha(150)  # Transparence
            overlay.fill((0, 0, 0))  # Noir
            blurred.blit(overlay, (0, 0))
            
            return blurred
        return None

    def run(self):
        while self.running:
            # Utiliser l'arrière-plan flouté ou la couleur par défaut
            if self.background_surface:
                blurred_bg = self.create_blurred_background()
                if blurred_bg:
                    self.screen.blit(blurred_bg, (0, 0))
                else:
                    self.screen.fill(COLOR_BG)
            else:
                self.screen.fill(COLOR_BG)
            
            # Dessiner le logo en bas à gauche
            draw_logo(self.screen, "bottom-left")
            
            mouse_pos = pygame.mouse.get_pos()

            button_rects = []
            for i, btn in enumerate(self.buttons):
                rect = pygame.Rect(
                    self.screen.get_width() // 2 - BUTTON_WIDTH // 2,
                    150 + i * (BUTTON_HEIGHT + 20),
                    BUTTON_WIDTH,
                    BUTTON_HEIGHT
                )
                hovered = rect.collidepoint(mouse_pos)
                if hovered:
                    self.hovered_index = i
                self.draw_button(btn["label"], rect, hovered, i)
                button_rects.append(rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return "quit"
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "resume"
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i, rect in enumerate(button_rects):
                        if rect.collidepoint(event.pos):
                            action = self.buttons[i]["action"]
                            if action == "resume":
                                return "resume"
                            elif action == "settings":
                                settings = SettingsMenu(self.screen)
                                settings.run()
                            elif action == "abandon":
                                return "abandon"
                            elif action == "menu":
                                return "menu"

            pygame.display.flip()
            self.clock.tick(60)