import pygame
import random
import sys
import time
from pause_menu import PauseMenu
from level_menu import mark_level_completed

def solve_animation_impossible(screen, tiles, current_order, grid_size, TILE_WIDTH, TILE_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT):
    """Animation pour le niveau impossible (100x100) - même principe mais plus rapide"""
    font = pygame.font.SysFont(None, 40)
    clock = pygame.time.Clock()
    
    # Animation text
    animation_text = font.render("Résolution automatique...", True, (255, 255, 0))
    
    # Créer une liste des positions à corriger dans un ordre aléatoire
    positions_to_fix = []
    for target_pos in range(len(tiles)):
        if current_order[target_pos] != target_pos:
            positions_to_fix.append(target_pos)
    
    # Mélanger pour un ordre aléatoire
    random.shuffle(positions_to_fix)
    
    # Traiter les pièces par groupes comme les autres niveaux
    batch_size = min(3, len(positions_to_fix))  # Même batch size que les autres
    
    for i in range(0, len(positions_to_fix), batch_size):
        batch = positions_to_fix[i:i+batch_size]
        
        # Animer le batch de pièces ULTRA rapidement
        animate_batch_movement_impossible(screen, tiles, current_order, batch, 
                                        grid_size, TILE_WIDTH, TILE_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT, animation_text)
        
        # Échanger toutes les pièces du batch
        for target_pos in batch:
            if current_order[target_pos] != target_pos:
                source_pos = current_order.index(target_pos)
                current_order[source_pos], current_order[target_pos] = current_order[target_pos], current_order[source_pos]
        
        # Pause TRÈS courte pour le 100x100
        pygame.time.wait(0)  # Seulement 100ms au lieu de 10ms

    # Animation finale normale
    celebration_animation(screen, tiles, grid_size, TILE_WIDTH, TILE_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT, "automatiquement")

def solve_animation(screen, tiles, tile_order, grid_size, TILE_WIDTH, TILE_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT):
    """Animation qui résout automatiquement le puzzle"""
    font = pygame.font.SysFont(None, 40)
    clock = pygame.time.Clock()
    
    # Créer une copie de l'ordre actuel pour l'animation
    current_order = tile_order.copy()
    
    # Animation text
    animation_text = font.render("Résolution automatique...", True, (255, 255, 0))
    
    # Pour le niveau impossible (100x100), utiliser une animation ultra-rapide spéciale
    if grid_size >= 50:  # Niveau impossible ou très difficile
        solve_animation_impossible(screen, tiles, current_order, grid_size, TILE_WIDTH, TILE_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT)
        return
    
    # Créer une liste des positions à corriger dans un ordre aléatoire
    positions_to_fix = []
    for target_pos in range(len(tiles)):
        if current_order[target_pos] != target_pos:
            positions_to_fix.append(target_pos)
    
    # Mélanger pour un ordre aléatoire
    random.shuffle(positions_to_fix)
    
    # Traiter les pièces par groupes pour plus de rapidité
    batch_size = min(3, len(positions_to_fix))  # Jusqu'à 3 pièces simultanément
    
    for i in range(0, len(positions_to_fix), batch_size):
        batch = positions_to_fix[i:i+batch_size]
        
        # Animer le batch de pièces simultanément
        animate_batch_movement(screen, tiles, current_order, batch, 
                             grid_size, TILE_WIDTH, TILE_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT, animation_text)
        
        # Échanger toutes les pièces du batch
        for target_pos in batch:
            if current_order[target_pos] != target_pos:
                source_pos = current_order.index(target_pos)
                current_order[source_pos], current_order[target_pos] = current_order[target_pos], current_order[source_pos]
        
        # Pause très courte entre chaque batch
        pygame.time.wait(10)  # Encore plus court pour les batches
    
    # Animation finale
    celebration_animation(screen, tiles, grid_size, TILE_WIDTH, TILE_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT, "automatiquement")

def celebration_animation(screen, tiles, grid_size, TILE_WIDTH, TILE_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT, solve_type=""):
    """Animation de célébration quand le puzzle est résolu"""
    font = pygame.font.SysFont(None, 40)
    clock = pygame.time.Clock()
    
    frame = 0
    waiting_for_input = False
    
    # Animation finale - afficher le puzzle résolu avec effets
    while True:
        screen.fill((0, 0, 0))
        
        # Afficher toutes les pièces à leur place finale
        for i in range(len(tiles)):
            row = i // grid_size
            col = i % grid_size
            x = col * TILE_WIDTH
            y = row * TILE_HEIGHT
            
            # Effet de scintillement seulement pendant les 3 premières secondes (180 frames)
            if frame < 180 and frame % 20 < 10:
                # Ajouter une bordure dorée scintillante
                pygame.draw.rect(screen, (255, 215, 0), (x-2, y-2, TILE_WIDTH+4, TILE_HEIGHT+4), 3)
            
            screen.blit(tiles[i], (x, y))
        
        # Messages avec effet de pulsation
        pulse = abs(sin(frame * 0.1)) * 50 + 205  # Pulsation entre 205 et 255
        color = (int(pulse), 255, int(pulse))
        
        if solve_type == "automatiquement":
            success_msg = font.render("Puzzle résolu automatiquement !", True, color)
            success_rect = success_msg.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
            
            # Cadre derrière le texte
            padding = 10
            frame_rect = success_rect.inflate(padding * 2, padding * 2)
            pygame.draw.rect(screen, (0, 0, 0, 128), frame_rect)  # Fond semi-transparent
            pygame.draw.rect(screen, (255, 255, 255), frame_rect, 2)  # Bordure blanche
            
            screen.blit(success_msg, success_rect)
        else:
            success_msg = font.render("Félicitations ! Puzzle terminé !", True, color)
            success_rect = success_msg.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
            
            # Cadre derrière le texte
            padding = 10
            frame_rect = success_rect.inflate(padding * 2, padding * 2)
            pygame.draw.rect(screen, (0, 0, 0, 128), frame_rect)  # Fond semi-transparent
            pygame.draw.rect(screen, (255, 255, 255), frame_rect, 2)  # Bordure blanche
            
            screen.blit(success_msg, success_rect)
        
        if frame > 60:  # Afficher après 1 seconde
            waiting_for_input = True
            continue_msg = font.render("Appuyez sur une touche pour continuer...", True, (255, 255, 255))
            continue_rect = continue_msg.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            
            # Cadre derrière le texte de continuation
            padding = 8
            frame_rect = continue_rect.inflate(padding * 2, padding * 2)
            pygame.draw.rect(screen, (0, 0, 0, 128), frame_rect)  # Fond semi-transparent
            pygame.draw.rect(screen, (200, 200, 200), frame_rect, 1)  # Bordure grise
            
            screen.blit(continue_msg, continue_rect)
        
        pygame.display.flip()
        clock.tick(60)
        
        # Vérifier les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif waiting_for_input and (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN):
                return
        
        frame += 1

# Importer sin pour l'effet de pulsation
from math import sin

def animate_batch_movement_impossible(screen, tiles, current_order, batch_positions, 
                                    grid_size, TILE_WIDTH, TILE_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT, animation_text):
    """Même animation que animate_batch_movement mais plus rapide pour le 100x100"""
    clock = pygame.time.Clock()
    
    # Calculer les mouvements pour toutes les pièces du batch
    movements = []
    for target_pos in batch_positions:
        if current_order[target_pos] != target_pos:
            source_pos = current_order.index(target_pos)
            
            # Positions de départ et d'arrivée
            source_row, source_col = source_pos // grid_size, source_pos % grid_size
            target_row, target_col = target_pos // grid_size, target_pos % grid_size
            
            start_x, start_y = source_col * TILE_WIDTH, source_row * TILE_HEIGHT
            end_x, end_y = target_col * TILE_WIDTH, target_row * TILE_HEIGHT
            
            movements.append({
                'source_pos': source_pos,
                'target_pos': target_pos,
                'start_x': start_x,
                'start_y': start_y,
                'end_x': end_x,
                'end_y': end_y,
                'tile_idx': current_order[source_pos]
            })
    
    # Animation ULTRA rapide (2 frames au lieu de 4)
    frames = 2
    for frame in range(frames):
        # Interpolation avec effet d'accélération
        t = frame / frames
        eased_t = t * t * (3.0 - 2.0 * t)  # Smooth step function
        
        # Effacer l'écran
        screen.fill((0, 0, 0))
        
        # Positions des pièces en mouvement pour éviter de les dessiner deux fois
        moving_positions = {mov['source_pos'] for mov in movements}
        
        # Afficher toutes les pièces fixes
        for i, tile_idx in enumerate(current_order):
            if i not in moving_positions:
                row = i // grid_size
                col = i % grid_size
                x = col * TILE_WIDTH
                y = row * TILE_HEIGHT
                screen.blit(tiles[tile_idx], (x, y))
        
        # Afficher toutes les pièces en mouvement
        for mov in movements:
            current_x = mov['start_x'] + (mov['end_x'] - mov['start_x']) * eased_t
            current_y = mov['start_y'] + (mov['end_y'] - mov['start_y']) * eased_t
            
            # Effet de surbrillance colorée différente pour chaque pièce
            colors = [(255, 255, 0), (0, 255, 255), (255, 0, 255)]  # Jaune, Cyan, Magenta
            color = colors[movements.index(mov) % len(colors)]
            
            pygame.draw.rect(screen, color, 
                           (int(current_x)-2, int(current_y)-2, TILE_WIDTH+4, TILE_HEIGHT+4), 3)
            
            screen.blit(tiles[mov['tile_idx']], (int(current_x), int(current_y)))
        
        # Afficher le texte d'animation
        screen.blit(animation_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(60)

def animate_batch_movement(screen, tiles, current_order, batch_positions, 
                          grid_size, TILE_WIDTH, TILE_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT, animation_text):
    """Anime le déplacement simultané de plusieurs pièces"""
    clock = pygame.time.Clock()
    
    # Calculer les mouvements pour toutes les pièces du batch
    movements = []
    for target_pos in batch_positions:
        if current_order[target_pos] != target_pos:
            source_pos = current_order.index(target_pos)
            
            # Positions de départ et d'arrivée
            source_row, source_col = source_pos // grid_size, source_pos % grid_size
            target_row, target_col = target_pos // grid_size, target_pos % grid_size
            
            start_x, start_y = source_col * TILE_WIDTH, source_row * TILE_HEIGHT
            end_x, end_y = target_col * TILE_WIDTH, target_row * TILE_HEIGHT
            
            movements.append({
                'source_pos': source_pos,
                'target_pos': target_pos,
                'start_x': start_x,
                'start_y': start_y,
                'end_x': end_x,
                'end_y': end_y,
                'tile_idx': current_order[source_pos]
            })
    
    # Animation super rapide (4 frames = 0.067 seconde à 60 FPS)
    frames = 4
    for frame in range(frames):
        # Interpolation avec effet d'accélération
        t = frame / frames
        eased_t = t * t * (3.0 - 2.0 * t)  # Smooth step function
        
        # Effacer l'écran
        screen.fill((0, 0, 0))
        
        # Positions des pièces en mouvement pour éviter de les dessiner deux fois
        moving_positions = {mov['source_pos'] for mov in movements}
        
        # Afficher toutes les pièces fixes
        for i, tile_idx in enumerate(current_order):
            if i not in moving_positions:
                row = i // grid_size
                col = i % grid_size
                x = col * TILE_WIDTH
                y = row * TILE_HEIGHT
                screen.blit(tiles[tile_idx], (x, y))
        
        # Afficher toutes les pièces en mouvement
        for mov in movements:
            current_x = mov['start_x'] + (mov['end_x'] - mov['start_x']) * eased_t
            current_y = mov['start_y'] + (mov['end_y'] - mov['start_y']) * eased_t
            
            # Effet de surbrillance colorée différente pour chaque pièce
            colors = [(255, 255, 0), (0, 255, 255), (255, 0, 255)]  # Jaune, Cyan, Magenta
            color = colors[movements.index(mov) % len(colors)]
            
            pygame.draw.rect(screen, color, 
                           (int(current_x)-2, int(current_y)-2, TILE_WIDTH+4, TILE_HEIGHT+4), 3)
            
            screen.blit(tiles[mov['tile_idx']], (int(current_x), int(current_y)))
        
        # Afficher le texte d'animation
        screen.blit(animation_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(60)

def animate_piece_movement_fast(screen, tiles, current_order, source_pos, target_pos, 
                               grid_size, TILE_WIDTH, TILE_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT, animation_text):
    """Anime rapidement le déplacement d'une pièce de source_pos vers target_pos"""
    clock = pygame.time.Clock()
    
    # Calculer les positions de départ et d'arrivée
    source_row, source_col = source_pos // grid_size, source_pos % grid_size
    target_row, target_col = target_pos // grid_size, target_pos % grid_size
    
    start_x, start_y = source_col * TILE_WIDTH, source_row * TILE_HEIGHT
    end_x, end_y = target_col * TILE_WIDTH, target_row * TILE_HEIGHT
    
    # Animation de mouvement très rapide (6 frames = 0.1 seconde à 60 FPS)
    frames = 6  # Réduit de 10 à 6 frames
    for frame in range(frames):
        # Interpolation avec effet d'accélération (easing)
        t = frame / frames
        # Courbe d'accélération pour un mouvement plus dynamique
        eased_t = t * t * (3.0 - 2.0 * t)  # Smooth step function
        
        current_x = start_x + (end_x - start_x) * eased_t
        current_y = start_y + (end_y - start_y) * eased_t
        
        # Effacer l'écran
        screen.fill((0, 0, 0))
        
        # Afficher toutes les pièces sauf celle en mouvement
        for i, tile_idx in enumerate(current_order):
            if i == source_pos:
                continue  # On ne dessine pas la pièce en mouvement ici
            
            row = i // grid_size
            col = i % grid_size
            x = col * TILE_WIDTH
            y = row * TILE_HEIGHT
            screen.blit(tiles[tile_idx], (x, y))
        
        # Afficher la pièce en mouvement à sa position interpolée avec un effet de surbrillance
        moving_piece = tiles[current_order[source_pos]]
        
        # Ajouter un effet de surbrillance pendant le mouvement
        highlight_color = (255, 255, 0)  # Jaune
        pygame.draw.rect(screen, highlight_color, 
                        (int(current_x)-2, int(current_y)-2, TILE_WIDTH+4, TILE_HEIGHT+4), 3)
        
        screen.blit(moving_piece, (int(current_x), int(current_y)))
        
        # Afficher le texte d'animation
        screen.blit(animation_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(60)

def animate_piece_movement(screen, tiles, current_order, source_pos, target_pos, 
                         grid_size, TILE_WIDTH, TILE_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT, animation_text):
    """Anime le déplacement d'une pièce de source_pos vers target_pos"""
    clock = pygame.time.Clock()
    
    # Calculer les positions de départ et d'arrivée
    source_row, source_col = source_pos // grid_size, source_pos % grid_size
    target_row, target_col = target_pos // grid_size, target_pos % grid_size
    
    start_x, start_y = source_col * TILE_WIDTH, source_row * TILE_HEIGHT
    end_x, end_y = target_col * TILE_WIDTH, target_row * TILE_HEIGHT
    
    # Animation de mouvement (30 frames = 0.5 seconde à 60 FPS)
    frames = 30
    for frame in range(frames):
        # Interpolation linéaire
        t = frame / frames
        current_x = start_x + (end_x - start_x) * t
        current_y = start_y + (end_y - start_y) * t
        
        # Effacer l'écran
        screen.fill((0, 0, 0))
        
        # Afficher toutes les pièces sauf celle en mouvement
        for i, tile_idx in enumerate(current_order):
            if i == source_pos:
                continue  # On ne dessine pas la pièce en mouvement ici
            
            row = i // grid_size
            col = i % grid_size
            x = col * TILE_WIDTH
            y = row * TILE_HEIGHT
            screen.blit(tiles[tile_idx], (x, y))
        
        # Afficher la pièce en mouvement à sa position interpolée
        moving_piece = tiles[current_order[source_pos]]
        screen.blit(moving_piece, (int(current_x), int(current_y)))
        
        # Afficher le texte d'animation
        screen.blit(animation_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(60)

def game_loop(screen, image_path, grid_size, difficulty_name=None, level_index=None):
    # Utiliser toute la taille de la fenêtre
    WINDOW_WIDTH = screen.get_width()  # 800
    WINDOW_HEIGHT = screen.get_height()  # 600
    
    # Calculer la taille des tuiles en fonction de la largeur (plus large)
    TILE_WIDTH = WINDOW_WIDTH // grid_size
    TILE_HEIGHT = WINDOW_HEIGHT // grid_size
    
    pygame.display.set_caption("Puzzle en cours...")

    # Charger et redimensionner l'image pour qu'elle remplisse toute la fenêtre
    original_image = pygame.image.load(image_path)
    original_image = pygame.transform.scale(original_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

    # Découper l'image
    def split_image(image):
        tiles = []
        for row in range(grid_size):
            for col in range(grid_size):
                rect = pygame.Rect(col * TILE_WIDTH, row * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)
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
                    pause_menu = PauseMenu(screen)
                    pause_action = pause_menu.run()
                    if pause_action == "menu":
                        return "menu"
                    elif pause_action == "quit":
                        return "quit"
                    elif pause_action == "abandon":
                        # Lancer l'animation de résolution automatique
                        solve_animation(screen, tiles, tile_order, grid_size, TILE_WIDTH, TILE_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT)
                        return "menu"
                    # sinon on continue (resume)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                col = mx // TILE_WIDTH
                row = my // TILE_HEIGHT
                index = row * grid_size + col
                if 0 <= index < len(tile_order):
                    selected_index = index
                    dragging = True
                    drag_offset = (mx - col * TILE_WIDTH, my - row * TILE_HEIGHT)

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if dragging:
                    mx, my = pygame.mouse.get_pos()
                    target_col = mx // TILE_WIDTH
                    target_row = my // TILE_HEIGHT
                    target_index = target_row * grid_size + target_col

                    if 0 <= target_index < len(tile_order):
                        tile_order[selected_index], tile_order[target_index] = tile_order[target_index], tile_order[selected_index]

                    dragging = False
                    selected_index = None

        # Affichage des tuiles
        for i, tile_idx in enumerate(tile_order):
            row = i // grid_size
            col = i % grid_size
            x = col * TILE_WIDTH
            y = row * TILE_HEIGHT

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
                
                # Afficher brièvement le message de victoire
                for _ in range(60):  # 1 seconde à 60 FPS
                    screen.fill((0, 0, 0))
                    
                    # Afficher toutes les pièces
                    for i, tile_idx in enumerate(tile_order):
                        row = i // grid_size
                        col = i % grid_size
                        x = col * TILE_WIDTH
                        y = row * TILE_HEIGHT
                        screen.blit(tiles[tile_idx], (x, y))
                    
                    # msg = font.render("Puzzle Résolu !", True, (0, 255, 0))
                    # msg_rect = msg.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30))
                    # screen.blit(msg, msg_rect)
                    
                    time_text = font.render(f"Temps: {final_time}s", True, (255, 255, 255))
                    screen.blit(time_text, (10, 10))
                    
                    pygame.display.flip()
                    clock.tick(60)
                
                # Lancer l'animation de célébration
                celebration_animation(screen, tiles, grid_size, TILE_WIDTH, TILE_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT)
                
                # Marquer le niveau comme terminé si c'est un niveau spécifique
                if difficulty_name is not None and level_index is not None:
                    is_new_record = mark_level_completed(difficulty_name, level_index, final_time)
                    if is_new_record:
                        # Afficher un message de nouveau record
                        record_font = pygame.font.SysFont(None, 48)
                        for i in range(90):  # 1.5 secondes supplémentaires
                            screen.fill((0, 0, 0))
                            
                            # Afficher toutes les pièces
                            for j, tile_idx in enumerate(tile_order):
                                row = j // grid_size
                                col = j % grid_size
                                x = col * TILE_WIDTH
                                y = row * TILE_HEIGHT
                                screen.blit(tiles[tile_idx], (x, y))
                            
                            # Message de nouveau record
                            record_text = record_font.render("NOUVEAU RECORD !", True, (255, 215, 0))  # Doré
                            record_rect = record_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
                            screen.blit(record_text, record_rect)
                            
                            time_text = font.render(f"Temps: {final_time}s", True, (255, 255, 255))
                            time_rect = time_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
                            screen.blit(time_text, time_rect)
                            
                            pygame.display.flip()
                            clock.tick(60)
                
                return "menu"

        # Afficher le chronomètre
        if not puzzle_solved:
            seconds = (pygame.time.get_ticks() - start_ticks) // 1000
        else:
            seconds = final_time

        time_text = font.render(f"Temps: {seconds}s", True, (255, 255, 255))
        screen.blit(time_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    # Le jeu retourne toujours "menu" quand on en sort
    return "menu"
