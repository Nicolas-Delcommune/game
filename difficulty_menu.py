# difficulty_menu.py
import pygame
import os
import random
from ui_theme import *
from level_menu import LevelMenu

class DifficultyMenu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(FONT_PATH, FONT_SIZE)
        self.title_font = pygame.font.Font(FONT_PATH, FONT_SIZE + 10)
        
        self.difficulties = [
            {"name": "Facile", "grid_size": 4, "description": "4x4 - 16 pièces"},
            {"name": "Moyen", "grid_size": 8, "description": "8x8 - 64 pièces"},
            {"name": "Difficile", "grid_size": 15, "description": "15x15 - 225 pièces"},
            {"name": "Impossible", "grid_size": 100, "description": "100x100 - 10000 pièces"}
        ]
        
        self.selected_index = 0

    def get_random_image(self):
        """Sélectionne une image aléatoire dans le dossier assets"""
        assets_path = "assets"
        if os.path.exists(assets_path):
            image_files = [f for f in os.listdir(assets_path) 
                          if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
            if image_files:
                return os.path.join(assets_path, random.choice(image_files))
        # Fallback vers une image par défaut
        return "assets/photo_1.jpg"

    def draw(self):
        self.screen.fill(COLOR_BG)
        
        # Dessiner le logo en bas à gauche
        draw_logo(self.screen, "bottom-left")
        
        # Titre
        title = self.title_font.render("Choisissez la difficulté", True, COLOR_TEXT)
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(title, title_rect)
        
        # Options de difficulté
        for index, difficulty in enumerate(self.difficulties):
            y_pos = 160 + index * 80  # Décalé vers le haut (était 200)
            
            # Couleur du texte selon la sélection
            if index == self.selected_index:
                text_color = get_difficulty_color(difficulty["name"])  # Couleur spécifique de la difficulté
                desc_color = get_difficulty_color(difficulty["name"])
            else:
                text_color = COLOR_TEXT
                desc_color = (150, 150, 150)
            
            # Dessiner des bandes de couleur à gauche ET à droite pour chaque difficulté
            band_color = get_difficulty_color(difficulty["name"])
            # Bande de gauche
            left_band_rect = pygame.Rect(50, y_pos - 30, 10, 60)
            pygame.draw.rect(self.screen, band_color, left_band_rect)
            # Bande de droite
            right_band_rect = pygame.Rect(self.screen.get_width() - 60, y_pos - 30, 10, 60)
            pygame.draw.rect(self.screen, band_color, right_band_rect)
            
            # Calculer la position pour centrer l'ensemble titre + description
            title_y = y_pos - 12  # Décaler le titre vers le haut
            desc_y = y_pos + 12   # Décaler la description vers le bas
            
            # Nom de la difficulté
            name_text = self.font.render(difficulty["name"], True, text_color)
            name_rect = name_text.get_rect(center=(self.screen.get_width() // 2, title_y))
            self.screen.blit(name_text, name_rect)
            
            # Description
            desc_font = pygame.font.Font(FONT_PATH, FONT_SIZE - 8)
            desc_text = desc_font.render(difficulty["description"], True, desc_color)
            desc_rect = desc_text.get_rect(center=(self.screen.get_width() // 2, desc_y))
            self.screen.blit(desc_text, desc_rect)

    def run(self):
        while True:
            self.draw()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit", None
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_index = (self.selected_index - 1) % len(self.difficulties)
                    elif event.key == pygame.K_DOWN:
                        self.selected_index = (self.selected_index + 1) % len(self.difficulties)
                    elif event.key == pygame.K_RETURN:
                        result = self.get_selection()
                        if result is not None:
                            return result
                    elif event.key == pygame.K_ESCAPE:
                        return "back", None
                        
                elif event.type == pygame.MOUSEMOTION:
                    self.update_selection_with_mouse(event.pos)
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        result = self.get_selection()
                        if result is not None:
                            return result

            self.clock.tick(60)

    def update_selection_with_mouse(self, mouse_pos):
        for index, difficulty in enumerate(self.difficulties):
            # Zone de clic pour chaque difficulté (ajustée aux nouvelles positions)
            y_start = 140 + index * 80  # Ajusté pour correspondre au nouveau y_pos - 20
            y_end = y_start + 70  # Plus grande zone pour couvrir le texte et la description
            if y_start <= mouse_pos[1] <= y_end:
                self.selected_index = index
                break

    def get_selection(self):
        selected_difficulty = self.difficulties[self.selected_index]
        
        # Ouvrir le menu de sélection de niveau
        level_menu = LevelMenu(self.screen, selected_difficulty["name"], selected_difficulty["grid_size"])
        result = level_menu.run()
        
        # Si l'utilisateur a sélectionné un niveau, retourner le résultat
        if result[0] == "start":
            return result
        elif result[0] == "back":
            # Retourner à la sélection de difficulté
            return None
        else:
            # Quit ou autre
            return result
