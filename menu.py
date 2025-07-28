import pygame
import os

def menu_loop(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 40)
    running = True

    images = ["assets/photo_1.jpg", "assets/photo_2.jpg"]
    selected_image = images[0]
    grid_size = 3  # par défaut

    while running:
        screen.fill((30, 30, 30))

        title = font.render("Jeu de Puzzle - Menu", True, (255, 255, 255))
        screen.blit(title, (250, 40))

        # Choix de l’image
        img_label = font.render("Image :", True, (200, 200, 200))
        screen.blit(img_label, (100, 120))
        for idx, path in enumerate(images):
            label = font.render(f"{os.path.basename(path)}", True, (0, 200, 255) if path == selected_image else (150, 150, 150))
            screen.blit(label, (120, 160 + idx * 40))

        # Choix de la difficulté
        diff_label = font.render("Difficulté :", True, (200, 200, 200))
        screen.blit(diff_label, (100, 280))

        diffs = {3: "Facile (3x3)", 4: "Moyen (4x4)", 5: "Difficile (5x5)"}
        for i, (size, name) in enumerate(diffs.items()):
            color = (0, 255, 100) if size == grid_size else (150, 150, 150)
            label = font.render(name, True, color)
            screen.blit(label, (120, 320 + i * 40))

        # Bouton démarrer
        start_btn = pygame.Rect(300, 500, 200, 50)
        pygame.draw.rect(screen, (0, 120, 255), start_btn)
        start_txt = font.render("Démarrer", True, (255, 255, 255))
        screen.blit(start_txt, (start_btn.x + 40, start_btn.y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                for idx, path in enumerate(images):
                    if 120 <= mx <= 500 and (160 + idx * 40) <= my <= (160 + idx * 40 + 30):
                        selected_image = path

                for i, size in enumerate(diffs.keys()):
                    if 120 <= mx <= 500 and (320 + i * 40) <= my <= (320 + i * 40 + 30):
                        grid_size = size

                if start_btn.collidepoint(mx, my):
                    return selected_image, grid_size

        clock.tick(30)
