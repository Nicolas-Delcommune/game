import pygame
from menu import menu_loop
from game import game_loop

pygame.init()

def main():
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Jeu de Puzzle")

    # Boucle principale : menu → jeu
    while True:
        params = menu_loop(screen)
        if params is None:
            break  # quitter le jeu

        image_path, grid_size = params
        result = game_loop(screen, image_path, grid_size)
        if result == "quit":
            break

    pygame.quit()

if __name__ == "__main__":
    main()
