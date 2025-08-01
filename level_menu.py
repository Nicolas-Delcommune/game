# level_menu.py
import pygame
import os
import json
from ui_theme import *

class LevelMenu:
    def __init__(self, screen, difficulty_name, grid_size):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(FONT_PATH, FONT_SIZE)
        self.title_font = pygame.font.Font(FONT_PATH, FONT_SIZE + 10)
        self.difficulty_name = difficulty_name
        self.grid_size = grid_size
        
        # Charger les images des niveaux
        self.levels = []
        self.thumbnails = []
        self.load_levels()
        
        # Charger la progression
        self.completed_levels = self.load_progress()
        
        self.selected_index = 0
        self.scroll_offset = 0

    def load_levels(self):
        """Charge les 10 niveaux (photo_1.jpg à photo_10.jpg)"""
        for i in range(1, 11):
            image_path = f"assets/photo_{i}.jpg"
            if os.path.exists(image_path):
                self.levels.append({
                    "name": f"Niveau {i}",
                    "image_path": image_path,
                    "thumbnail": self.create_thumbnail(image_path)
                })

    def create_thumbnail(self, image_path):
        """Crée une miniature de l'image"""
        try:
            image = pygame.image.load(image_path)
            # Redimensionner en miniature plus grande (100x75 pixels)
            thumbnail = pygame.transform.scale(image, (100, 75))
            return thumbnail
        except:
            # Image par défaut si erreur
            thumbnail = pygame.Surface((100, 75))
            thumbnail.fill((100, 100, 100))
            return thumbnail

    def load_progress(self):
        """Charge la progression des niveaux terminés avec leurs temps"""
        try:
            if os.path.exists("progress.json"):
                with open("progress.json", "r") as f:
                    progress = json.load(f)
                    difficulty_progress = progress.get(self.difficulty_name, {})
                    
                    # Convertir les clés en entiers et retourner un dictionnaire {niveau: temps}
                    completed_times = {}
                    if isinstance(difficulty_progress, list):
                        # Ancien format (liste) - ne pas afficher de temps par défaut
                        # On ignore simplement les anciens records sans temps
                        pass
                    else:
                        # Nouveau format (dictionnaire)
                        for level_key, time_value in difficulty_progress.items():
                            # Ignorer les temps par défaut de 999
                            if time_value != 999:
                                completed_times[int(level_key)] = time_value
                    
                    return completed_times
            return {}
        except:
            return {}

    def save_progress(self):
        """Sauvegarde la progression"""
        try:
            progress = {}
            if os.path.exists("progress.json"):
                with open("progress.json", "r") as f:
                    progress = json.load(f)
            
            # Convertir le dictionnaire de temps en format sauvegarde
            progress[self.difficulty_name] = {}
            for level_idx, time_value in self.completed_levels.items():
                progress[self.difficulty_name][str(level_idx)] = time_value
            
            with open("progress.json", "w") as f:
                json.dump(progress, f)
        except:
            pass

    def draw(self):
        self.screen.fill(COLOR_BG)
        
        # Dessiner les contours de la fenêtre avec la couleur de difficulté
        difficulty_color = get_difficulty_color(self.difficulty_name)
        border_width = 8
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        # Contours extérieurs avec la couleur de difficulté
        pygame.draw.rect(self.screen, difficulty_color, (0, 0, screen_width, border_width))  # Haut
        pygame.draw.rect(self.screen, difficulty_color, (0, screen_height - border_width, screen_width, border_width))  # Bas
        pygame.draw.rect(self.screen, difficulty_color, (0, 0, border_width, screen_height))  # Gauche
        pygame.draw.rect(self.screen, difficulty_color, (screen_width - border_width, 0, border_width, screen_height))  # Droite
        
        # Dessiner le logo en bas à gauche
        draw_logo(self.screen, "bottom-left")
        
        # Dessiner une bande de couleur en haut selon la difficulté
        difficulty_color = get_difficulty_color(self.difficulty_name)
        band_rect = pygame.Rect(0, 0, self.screen.get_width(), 8)
        pygame.draw.rect(self.screen, difficulty_color, band_rect)
        
        # Titre
        title = self.title_font.render(f"Niveaux - {self.difficulty_name}", True, COLOR_TEXT)
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(title, title_rect)
        
        # Instructions
        instruction = self.font.render("Choisissez votre niveau :", True, (200, 200, 200))
        instruction_rect = instruction.get_rect(center=(self.screen.get_width() // 2, 90))
        self.screen.blit(instruction, instruction_rect)
        
        # Grille des niveaux (5 colonnes, 2 lignes) - mieux centrée et plus large
        grid_width = 5 * 140  # Espacement plus large entre les colonnes
        grid_height = 2 * 140  # Espacement plus large entre les lignes
        start_x = (self.screen.get_width() - grid_width) // 2 + 70  # Centrer + décaler pour le centre des images
        start_y = (self.screen.get_height() - grid_height) // 2 + 40  # Centrer verticalement avec offset pour le titre
        
        for i, level in enumerate(self.levels):
            col = i % 5  # 5 colonnes
            row = i // 5  # 2 lignes
            
            x = start_x + col * 140  # Espacement horizontal plus large
            y = start_y + row * 140  # Espacement vertical plus large
            
            # Rectangle de sélection - parfaitement aligné sur l'image plus grande
            level_rect = pygame.Rect(x - 50, y - 37, 100, 75)  # Taille exacte de la miniature agrandie
            
            # Couleur de fond selon la sélection
            if i == self.selected_index:
                pygame.draw.rect(self.screen, COLOR_SELECTED, level_rect, 3)
                pygame.draw.rect(self.screen, (50, 50, 50), level_rect)
            else:
                pygame.draw.rect(self.screen, (30, 30, 30), level_rect)
                pygame.draw.rect(self.screen, (100, 100, 100), level_rect, 1)
            
            # Miniature de l'image - centrée dans le rectangle
            thumbnail_rect = level["thumbnail"].get_rect()
            thumbnail_rect.center = (x, y)
            self.screen.blit(level["thumbnail"], thumbnail_rect)
            
            # Si le niveau est terminé, appliquer un filtre et afficher le temps
            if i in self.completed_levels:
                # Filtre de couleur de la difficulté semi-transparent
                difficulty_color = get_difficulty_color(self.difficulty_name)
                overlay_surface = pygame.Surface((100, 75))
                overlay_surface.fill(difficulty_color)
                overlay_surface.set_alpha(150)
                self.screen.blit(overlay_surface, thumbnail_rect)
                
                # Temps de completion au centre avec texte noir sur fond coloré
                completion_time = self.completed_levels[i]
                time_font = pygame.font.SysFont('Arial', 20, bold=True)
                time_text = time_font.render(f"{completion_time}s", True, (0, 0, 0))  # Texte noir
                
                # Créer un fond coloré pour le texte
                text_bg_width = time_text.get_width() + 10
                text_bg_height = time_text.get_height() + 4
                text_bg = pygame.Surface((text_bg_width, text_bg_height))
                text_bg.fill(difficulty_color)
                
                # Centrer le fond et le texte
                bg_rect = text_bg.get_rect(center=(x, y))
                text_rect = time_text.get_rect(center=(x, y))
                
                self.screen.blit(text_bg, bg_rect)
                self.screen.blit(time_text, text_rect)
            
            # Nom du niveau
            if i == self.selected_index:
                # Niveau sélectionné : couleur de la difficulté
                level_color = get_difficulty_color(self.difficulty_name)
            else:
                # Niveau non sélectionné : couleur normale
                level_color = (150, 150, 150)
            level_text = self.font.render(level["name"], True, level_color)
            level_text_rect = level_text.get_rect(center=(x, y + 50))
            self.screen.blit(level_text, level_text_rect)

    def run(self):
        while True:
            self.draw()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit", None
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if self.selected_index > 0:
                            self.selected_index -= 1
                    elif event.key == pygame.K_RIGHT:
                        if self.selected_index < len(self.levels) - 1:
                            self.selected_index += 1
                    elif event.key == pygame.K_UP:
                        if self.selected_index >= 5:  # Si on n'est pas sur la première ligne
                            self.selected_index -= 5
                    elif event.key == pygame.K_DOWN:
                        if self.selected_index < 5:  # Si on est sur la première ligne
                            self.selected_index += 5
                    elif event.key == pygame.K_RETURN:
                        return self.get_selection()
                    elif event.key == pygame.K_ESCAPE:
                        return "back", None
                        
                elif event.type == pygame.MOUSEMOTION:
                    self.update_selection_with_mouse(event.pos)
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        return self.get_selection()

            self.clock.tick(60)

    def update_selection_with_mouse(self, mouse_pos):
        grid_width = 5 * 140
        grid_height = 2 * 140
        start_x = (self.screen.get_width() - grid_width) // 2 + 70
        start_y = (self.screen.get_height() - grid_height) // 2 + 40
        
        for i, level in enumerate(self.levels):
            col = i % 5
            row = i // 5
            
            x = start_x + col * 140
            y = start_y + row * 140
            
            # Zone de clic pour chaque niveau (centrée sur l'image)
            level_rect = pygame.Rect(x - 70, y - 70, 140, 120)
            if level_rect.collidepoint(mouse_pos):
                self.selected_index = i
                break

    def get_selection(self):
        if 0 <= self.selected_index < len(self.levels):
            selected_level = self.levels[self.selected_index]
            return "start", (selected_level["image_path"], self.grid_size, self.difficulty_name, self.selected_index)
        return "back", None

# Fonction utilitaire pour marquer un niveau comme terminé depuis n'importe où
def mark_level_completed(difficulty_name, level_index, completion_time=None):
    """Marque un niveau comme terminé et sauvegarde la progression avec le temps
    Retourne True si c'est un nouveau record, False sinon"""
    try:
        progress = {}
        if os.path.exists("progress.json"):
            with open("progress.json", "r") as f:
                progress = json.load(f)
        
        if difficulty_name not in progress:
            progress[difficulty_name] = {}
        
        # Stocker le temps de completion (ou garder l'ancien si meilleur)
        level_key = str(level_index)
        is_new_record = False
        
        if completion_time is not None:
            if level_key not in progress[difficulty_name]:
                # Premier completion du niveau
                progress[difficulty_name][level_key] = completion_time
                is_new_record = True
            elif completion_time < progress[difficulty_name][level_key]:
                # Nouveau record !
                progress[difficulty_name][level_key] = completion_time
                is_new_record = True
            # Sinon, on garde l'ancien temps (meilleur)
        # Suppression du cas "else" - on ne sauvegarde que si on a un temps réel
        
        with open("progress.json", "w") as f:
            json.dump(progress, f)
            
        return is_new_record
    except:
        return False
