import pygame
import random
import sys

def game_loop(screen, image_path, grid_size):
    TILE_SIZE = 600 // grid_size
    WINDOW_SIZE = TILE_SIZE * grid_size
    pygame.display.set_caption("Puzzle en cours...")

    # Charger et redimensionner l'image
    original_image = pygame.image.load(image_path)
    original_image = pygame.transform.scale(original_image, (WINDOW_SIZE, WINDOW_SIZE))

    # Découper l'image
    def split_image(image):
        tiles = []
        for row in range(grid_size):
            for col in range(grid_size):
                rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                tile = image.subsurface(rect).copy()
                tiles.append(tile)
        return tiles

    # Initialisation des données
    tiles = split_image(original_image)
    tile_order = list(range(len(tiles)))
    random.shuffle(tile_order)

    selected_index = None
    dragging = False
    drag_offset = (0, 0)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 40)

    # Chronomètre
    start_ticks = pygame.time.get_ticks()
    puzzle_solved = False

    while True:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_action = show_pause_menu(screen)
                    if pause_action == "menu":
                        return "menu"
                    elif pause_action == "quit":
                        return "quit"
                    # sinon on continue (resume / params)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                col = mx // TILE_SIZE
                row = my // TILE_SIZE
                index = row * grid_size + col
                if 0 <= index < len(tile_order):
                    selected_index = index
                    dragging = True
                    drag_offset = (mx - col * TILE_SIZE, my - row * TILE_SIZE)

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if dragging:
                    mx, my = pygame.mouse.get_pos()
                    target_col = mx // TILE_SIZE
                    target_row = my // TILE_SIZE
                    target_index = target_row * grid_size + target_col

                    if 0 <= target_index < len(tile_order):
                        tile_order[selected_index], tile_order[target_index] = tile_order[target_index], tile_order[selected_index]

                    dragging = False
                    selected_index = None

        # Affichage des tuiles
        for i, tile_idx in enumerate(tile_order):
            row = i // grid_size
            col = i % grid_size
            x = col * TILE_SIZE
            y = row * TILE_SIZE

            if dragging and i == selected_index:
                continue
            screen.blit(tiles[tile_idx], (x, y))

        # Dessin de la tuile glissée
        if dragging and selected_index is not None:
            mx, my = pygame.mouse.get_pos()
            tile = tiles[tile_order[selected_index]]
            screen.blit(tile, (mx - drag_offset[0], my - drag_offset[1]))

        # Vérifier si le puzzle est résolu
        if tile_order == list(range(len(tiles))):
            if not puzzle_solved:
                puzzle_solved = True
                final_time = (pygame.time.get_ticks() - start_ticks) // 1000

            msg = font.render("🎉 Puzzle Résolu !", True, (0, 255, 0))
            screen.blit(msg, (WINDOW_SIZE // 2 - 180, WINDOW_SIZE // 2 - 30))

        # Afficher le chronomètre
        if not puzzle_solved:
            seconds = (pygame.time.get_ticks() - start_ticks) // 1000
        else:
            seconds = final_time

        time_text = font.render(f"⏱️ {seconds}s", True, (255, 255, 255))
        screen.blit(time_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

def show_pause_menu(screen):
    menu_font = pygame.font.SysFont(None, 50)
    selected = 0
    options = ["Reprendre", "Paramètres", "Retour au menu"]
    clock = pygame.time.Clock()

    while True:
        screen.fill((20, 20, 20))
        title = menu_font.render("⏸️ Pause", True, (255, 255, 255))
        screen.blit(title, (screen.get_width() // 2 - 80, 80))

        mouse_pos = pygame.mouse.get_pos()

        for i, text in enumerate(options):
            # Calculer le rectangle du texte pour détection souris
            option_surface = menu_font.render(text, True, (255, 255, 255))
            option_rect = option_surface.get_rect()
            option_rect.topleft = (screen.get_width() // 2 - 120, 180 + i * 60)

            # Si souris survol
            if option_rect.collidepoint(mouse_pos):
                selected = i

            color = (255, 255, 0) if i == selected else (200, 200, 200)
            option = menu_font.render(text, True, color)
            screen.blit(option, option_rect.topleft)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if options[selected] == "Reprendre":
                        return "resume"
                    elif options[selected] == "Paramètres":
                        return "params"
                    elif options[selected] == "Retour au menu":
                        return "menu"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Clic gauche : valider l'option sélectionnée
                return {
                    "Reprendre": "resume",
                    "Paramètres": "params",
                    "Retour au menu": "menu"
                }[options[selected]]

        clock.tick(30)
