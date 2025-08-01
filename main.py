# main.py
import pygame
import os
from menu import Menu
from game import game_loop
from music_manager import music_manager

pygame.init()

# Obtenir les dimensions de l'écran et créer une fenêtre de cette taille (mais pas en plein écran)
info = pygame.display.Info()
SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 700

# Créer la fenêtre avec la taille de l'écran mais en mode fenêtré
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jeu de Puzzle")

def main():
    # Démarrer la musique de fond
    music_manager.play_music()
    
    running = True
    while running:
        menu = Menu(screen)
        action, params = menu.run()  # ← modifié pour retourner image et difficulté
        if action == "start":
            if len(params) == 4:  # Nouveau format avec niveau
                image_path, grid_size, difficulty_name, level_index = params
                game_result = game_loop(screen, image_path, grid_size, difficulty_name, level_index)
                # Après avoir terminé un niveau, on recharge pour voir les nouveaux temps
            else:  # Ancien format pour compatibilité
                image_path, grid_size = params
                game_result = game_loop(screen, image_path, grid_size)
            pygame.display.set_caption("Jeu de Puzzle")
            if game_result == "quit":
                running = False
        elif action == "quit":
            running = False
        elif action == "back":
            # Retour du menu de difficulté vers le menu principal
            continue

    pygame.quit()

if __name__ == "__main__":
    main()
