# settings_menu.py
import pygame
import json
from ui_theme import *
from music_manager import music_manager

def load_settings():
    """Charger les paramètres depuis le fichier JSON"""
    try:
        with open('settings.json', 'r') as f:
            return json.load(f)
    except:
        return {"volume": 0.5, "fullscreen": False}

def save_settings(settings):
    """Sauvegarder les paramètres dans le fichier JSON"""
    try:
        with open('settings.json', 'w') as f:
            json.dump(settings, f)
    except:
        pass

class SettingsMenu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(FONT_PATH, FONT_SIZE)
        self.title_font = pygame.font.Font(FONT_PATH, FONT_SIZE + 10)
        self.options = ["Volume", "Plein écran", "Retour"]
        self.selected_index = -1  # Aucune sélection par défaut
        self.settings = load_settings()
        self.dragging_volume = False  # Pour suivre si on glisse sur la barre de volume

    def draw(self):
        self.screen.fill(COLOR_BG)
        
        # Titre
        title = self.title_font.render("Paramètres", True, COLOR_TEXT)
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(title, title_rect)
        
        for index, option in enumerate(self.options):
            is_selected = (index == self.selected_index and self.selected_index >= 0)
            color = COLOR_SELECTED if is_selected else COLOR_TEXT
            y_pos = 200 + index * 120  # Augmenté de 80 à 120 pour plus d'espacement
            
            if option == "Volume":
                # Affichage du volume avec barre de progression
                volume_text = self.font.render(f"Volume: {int(music_manager.get_volume() * 100)}%", True, color)
                volume_rect = volume_text.get_rect(center=(self.screen.get_width() // 2, y_pos))
                self.screen.blit(volume_text, volume_rect)
                
                # Barre de volume plus grande et plus visible
                bar_width = 400
                bar_height = 25
                bar_x = (self.screen.get_width() - bar_width) // 2
                bar_y = y_pos + 40
                
                # Fond de la barre avec bordure
                pygame.draw.rect(self.screen, (30, 30, 30), (bar_x, bar_y, bar_width, bar_height))
                pygame.draw.rect(self.screen, (200, 200, 200), (bar_x, bar_y, bar_width, bar_height), 3)
                
                # Barre de progression
                fill_width = int(bar_width * music_manager.get_volume())
                if fill_width > 0:
                    pygame.draw.rect(self.screen, COLOR_SELECTED, (bar_x, bar_y, fill_width, bar_height))
                
                # Curseur de volume
                cursor_x = bar_x + fill_width - 5
                cursor_y = bar_y - 5
                pygame.draw.rect(self.screen, (255, 255, 255), (cursor_x, cursor_y, 10, bar_height + 10))
                pygame.draw.rect(self.screen, (100, 100, 100), (cursor_x, cursor_y, 10, bar_height + 10), 2)
                
                # Instructions
                if is_selected:
                    instruction = pygame.font.Font(FONT_PATH, FONT_SIZE - 8).render(
                        "Cliquez sur la barre pour ajuster le volume", True, (150, 150, 150)
                    )
                    instruction_rect = instruction.get_rect(center=(self.screen.get_width() // 2, y_pos + 80))
                    self.screen.blit(instruction, instruction_rect)
                
                # Stocker la position de la barre pour la détection de clic
                if not hasattr(self, 'volume_bar_rect'):
                    self.volume_bar_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
            elif option == "Plein écran":
                # Affichage du toggle plein écran avec bouton visuel
                fullscreen_text = self.font.render("Plein écran:", True, color)
                text_rect = fullscreen_text.get_rect(center=(self.screen.get_width() // 2 - 50, y_pos))
                self.screen.blit(fullscreen_text, text_rect)
                
                # Bouton toggle visuel
                toggle_width = 60
                toggle_height = 30
                toggle_x = self.screen.get_width() // 2 + 20
                toggle_y = y_pos - toggle_height // 2
                
                # Couleur du bouton selon l'état
                is_fullscreen = self.settings.get("fullscreen", False)
                button_color = (50, 200, 50) if is_fullscreen else (200, 50, 50)
                border_color = (100, 255, 100) if is_fullscreen else (255, 100, 100)
                
                # Dessiner le bouton toggle
                pygame.draw.rect(self.screen, button_color, (toggle_x, toggle_y, toggle_width, toggle_height), border_radius=15)
                pygame.draw.rect(self.screen, border_color, (toggle_x, toggle_y, toggle_width, toggle_height), 3, border_radius=15)
                
                # Texte ON/OFF
                toggle_text = "ON" if is_fullscreen else "OFF"
                toggle_font = pygame.font.Font(FONT_PATH, FONT_SIZE - 8)
                toggle_surface = toggle_font.render(toggle_text, True, (255, 255, 255))
                toggle_text_rect = toggle_surface.get_rect(center=(toggle_x + toggle_width // 2, toggle_y + toggle_height // 2))
                self.screen.blit(toggle_surface, toggle_text_rect)
                
                # Instructions
                if is_selected:
                    instruction = pygame.font.Font(FONT_PATH, FONT_SIZE - 8).render(
                        "Cliquez sur le bouton pour basculer", True, (150, 150, 150)
                    )
                    instruction_rect = instruction.get_rect(center=(self.screen.get_width() // 2, y_pos + 40))
                    self.screen.blit(instruction, instruction_rect)
                
                # Stocker la position du bouton pour la détection de clic
                if not hasattr(self, 'fullscreen_button_rect'):
                    self.fullscreen_button_rect = pygame.Rect(toggle_x, toggle_y, toggle_width, toggle_height)
            else:
                # Affichage normal pour les autres options
                text = self.font.render(option, True, color)
                rect = text.get_rect(center=(self.screen.get_width() // 2, y_pos))
                self.screen.blit(text, rect)
    
    def toggle_fullscreen(self):
        """Basculer entre fenêtré et plein écran"""
        if self.settings.get("fullscreen", False):
            # Passer en plein écran
            info = pygame.display.Info()
            pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
        else:
            # Passer en mode fenêtré avec les dimensions définies dans main.py
            pygame.display.set_mode((1300, 700))
        
        # Mettre à jour la référence d'écran
        self.screen = pygame.display.get_surface()

    def run(self):
        running = True
        while running:
            self.draw()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                elif event.type == pygame.MOUSEMOTION:
                    self.update_selection_with_mouse(event.pos)
                    # Si on glisse sur la barre de volume, ajuster le volume
                    if self.dragging_volume and hasattr(self, 'volume_bar_rect'):
                        if self.volume_bar_rect.collidepoint(event.pos):
                            relative_x = event.pos[0] - self.volume_bar_rect.x
                            new_volume = max(0.0, min(1.0, relative_x / self.volume_bar_rect.width))
                            music_manager.set_volume(new_volume)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # Vérifier si clic sur la barre de volume
                        if hasattr(self, 'volume_bar_rect') and self.volume_bar_rect.collidepoint(event.pos):
                            self.dragging_volume = True
                            # Calculer le nouveau volume basé sur la position de la souris
                            relative_x = event.pos[0] - self.volume_bar_rect.x
                            new_volume = max(0.0, min(1.0, relative_x / self.volume_bar_rect.width))
                            music_manager.set_volume(new_volume)
                        # Vérifier si clic sur le bouton toggle plein écran
                        elif hasattr(self, 'fullscreen_button_rect') and self.fullscreen_button_rect.collidepoint(event.pos):
                            self.settings["fullscreen"] = not self.settings.get("fullscreen", False)
                            save_settings(self.settings)
                            self.toggle_fullscreen()
                        # Vérifier si clic sur le bouton Retour
                        else:
                            # Vérifier si on a cliqué sur "Retour"
                            for index, option in enumerate(self.options):
                                if option == "Retour":
                                    y_pos = 200 + index * 120
                                    text = self.font.render(option, True, COLOR_TEXT)
                                    rect = text.get_rect(center=(self.screen.get_width() // 2, y_pos))
                                    expanded_rect = pygame.Rect(rect.left - 50, rect.top - 20, rect.width + 100, rect.height + 40)
                                    if expanded_rect.collidepoint(event.pos):
                                        return
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.dragging_volume = False

            self.clock.tick(60)

    def update_selection_with_mouse(self, mouse_pos):
        old_selection = self.selected_index
        self.selected_index = -1  # Aucune sélection par défaut
        
        for index, option in enumerate(self.options):
            y_pos = 200 + index * 120  # Coordonnées mises à jour
            
            if option == "Volume":
                # Zone de clic pour le volume (inclut la barre)
                volume_rect = pygame.Rect(self.screen.get_width() // 2 - 200, y_pos - 30, 400, 120)
                if volume_rect.collidepoint(mouse_pos):
                    self.selected_index = index
            elif option == "Plein écran":
                # Zone de clic pour le plein écran (inclut le bouton toggle)
                fullscreen_rect = pygame.Rect(self.screen.get_width() // 2 - 100, y_pos - 30, 200, 80)
                if fullscreen_rect.collidepoint(mouse_pos):
                    self.selected_index = index
            else:
                # Zone de clic pour les autres options (Retour)
                text = self.font.render(option, True, COLOR_TEXT)
                rect = text.get_rect(center=(self.screen.get_width() // 2, y_pos))
                expanded_rect = pygame.Rect(rect.left - 50, rect.top - 20, rect.width + 100, rect.height + 40)
                if expanded_rect.collidepoint(mouse_pos):
                    self.selected_index = index
