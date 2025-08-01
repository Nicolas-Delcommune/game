import pygame
import random
import sys
import time
from pause_menu import PauseMenu
from level_menu import mark_level_completed
from ui_theme import get_difficulty_color

def draw_piece_outline(screen, piece_surface, x, y, color, thickness=2):
    """Dessine un contour qui épouse parfaitement la forme d'une pièce de puzzle"""
    # Créer un masque de la pièce pour détecter ses contours
    piece_mask = pygame.mask.from_surface(piece_surface)
    
    # Obtenir les contours de la pièce
    outline_points = piece_mask.outline()
    
    if len(outline_points) > 2:
        # Ajuster les points selon la position de la pièce
        adjusted_points = [(x + point[0], y + point[1]) for point in outline_points]
        
        # Dessiner le contour en reliant tous les points
        for i in range(thickness):
            offset_points = [(px + i, py + i) for px, py in adjusted_points]
            if len(offset_points) > 2:
                pygame.draw.polygon(screen, color, offset_points, 1)

def create_wood_texture(width, height):
    """Crée une surface avec une texture bois simulée"""
    wood_surface = pygame.Surface((width, height))
    
    # Couleurs de base du bois
    base_color = (139, 90, 43)  # Marron bois
    dark_color = (101, 67, 33)  # Marron foncé
    light_color = (160, 110, 60)  # Marron clair
    
    # Remplir avec la couleur de base
    wood_surface.fill(base_color)
    
    # Ajouter des lignes horizontales pour simuler le grain du bois
    for y in range(0, height, 3):
        color_variation = random.randint(-20, 20)
        line_color = tuple(max(0, min(255, c + color_variation)) for c in base_color)
        pygame.draw.line(wood_surface, line_color, (0, y), (width, y))
    
    # Ajouter quelques veines plus prononcées
    for _ in range(height // 20):
        y = random.randint(0, height)
        vein_color = dark_color if random.choice([True, False]) else light_color
        thickness = random.randint(1, 3)
        for i in range(thickness):
            if y + i < height:
                pygame.draw.line(wood_surface, vein_color, (0, y + i), (width, y + i))
    
    return wood_surface

def generate_puzzle_connections(grid_size):
    """Génère une carte des connexions entre pièces adjacentes"""
    # Structure: connections[row][col] = {'top': bool, 'right': bool, 'bottom': bool, 'left': bool}
    # True = protubérance, False = encoche, None = bord plat
    connections = {}
    
    for row in range(grid_size):
        connections[row] = {}
        for col in range(grid_size):
            connections[row][col] = {
                'top': None,
                'right': None, 
                'bottom': None,
                'left': None
            }
    
    # Générer les connexions horizontales (gauche-droite)
    for row in range(grid_size):
        for col in range(grid_size - 1):  # Pas la dernière colonne
            # Générer aléatoirement si la connexion est une protubérance ou encoche
            is_protrusion = random.choice([True, False])
            # La pièce de gauche a la forme, celle de droite a l'inverse
            connections[row][col]['right'] = is_protrusion
            connections[row][col + 1]['left'] = not is_protrusion
    
    # Générer les connexions verticales (haut-bas)  
    for row in range(grid_size - 1):  # Pas la dernière ligne
        for col in range(grid_size):
            # Générer aléatoirement si la connexion est une protubérance ou encoche
            is_protrusion = random.choice([True, False])
            # La pièce du haut a la forme, celle du bas a l'inverse
            connections[row][col]['bottom'] = is_protrusion
            connections[row + 1][col]['top'] = not is_protrusion
    
    return connections

def create_puzzle_piece_mask(extended_width, extended_height, base_width, base_height, padding, row, col, connections):
    """Crée un masque pour une pièce de puzzle en utilisant la carte des connexions"""
    # Commencer par un masque noir (transparent)
    mask = pygame.Surface((extended_width, extended_height), pygame.SRCALPHA)
    mask.fill((0, 0, 0, 0))  # Complètement transparent
    
    # Dessiner la forme de base de la pièce en blanc (opaque) au centre
    pygame.draw.rect(mask, (255, 255, 255, 255), (padding, padding, base_width, base_height))
    
    # Taille des encoches/protubérances
    bump_radius = min(base_width, base_height) // 6
    
    piece_connections = connections[row][col]
    
    # Côté haut
    if piece_connections['top'] is not None:  # Pas un bord
        center_x = padding + base_width // 2
        if piece_connections['top']:  # Protubérance vers le haut
            pygame.draw.circle(mask, (255, 255, 255, 255), 
                             (center_x, padding - bump_radius//2), bump_radius)
        else:  # Encoche vers l'intérieur
            pygame.draw.circle(mask, (0, 0, 0, 0), 
                             (center_x, padding + bump_radius//2), bump_radius)
    
    # Côté bas
    if piece_connections['bottom'] is not None:  # Pas un bord
        center_x = padding + base_width // 2
        if piece_connections['bottom']:  # Protubérance vers le bas
            pygame.draw.circle(mask, (255, 255, 255, 255), 
                             (center_x, padding + base_height + bump_radius//2), bump_radius)
        else:  # Encoche vers l'intérieur
            pygame.draw.circle(mask, (0, 0, 0, 0), 
                             (center_x, padding + base_height - bump_radius//2), bump_radius)
    
    # Côté gauche
    if piece_connections['left'] is not None:  # Pas un bord
        center_y = padding + base_height // 2
        if piece_connections['left']:  # Protubérance vers la gauche
            pygame.draw.circle(mask, (255, 255, 255, 255), 
                             (padding - bump_radius//2, center_y), bump_radius)
        else:  # Encoche vers l'intérieur
            pygame.draw.circle(mask, (0, 0, 0, 0), 
                             (padding + bump_radius//2, center_y), bump_radius)
    
    # Côté droit
    if piece_connections['right'] is not None:  # Pas un bord
        center_y = padding + base_height // 2
        if piece_connections['right']:  # Protubérance vers la droite
            pygame.draw.circle(mask, (255, 255, 255, 255), 
                             (padding + base_width + bump_radius//2, center_y), bump_radius)
        else:  # Encoche vers l'intérieur
            pygame.draw.circle(mask, (0, 0, 0, 0), 
                             (padding + base_width - bump_radius//2, center_y), bump_radius)
    
    return mask

def celebration_animation(screen, tiles, grid_size, puzzle_area, difficulty_name="", solve_type=""):
    """Animation de célébration quand le puzzle est résolu"""
    font = pygame.font.SysFont(None, 48)
    clock = pygame.time.Clock()
    
    frame = 0
    waiting_for_input = False
    
    while frame < 180 or waiting_for_input:  # 3 secondes + attente
        if frame < 120:
            # Phase 1: Animation des pièces qui brillent
            screen.fill((40, 40, 40))  # Fond gris foncé
            
            # Dessiner le cadre du puzzle
            puzzle_x, puzzle_y, puzzle_width, puzzle_height = puzzle_area
            pygame.draw.rect(screen, (200, 200, 200), (puzzle_x-2, puzzle_y-2, puzzle_width+4, puzzle_height+4), 2)
            
            # Calculer la taille des pièces
            tile_width = puzzle_width // grid_size
            tile_height = puzzle_height // grid_size
            
            # Afficher toutes les pièces avec effet de brillance
            for i, tile in enumerate(tiles):
                row = i // grid_size
                col = i % grid_size
                x = puzzle_x + col * tile_width
                y = puzzle_y + row * tile_height
                
                # Effet de brillance aléatoire
                if random.randint(0, 10) < 3:
                    difficulty_color = get_difficulty_color(difficulty_name) if difficulty_name else (255, 215, 0)
                    pygame.draw.rect(screen, difficulty_color, (x-2, y-2, tile_width+4, tile_height+4), 3)
                
                screen.blit(pygame.transform.scale(tile, (tile_width, tile_height)), (x, y))
            
            # Message de succès
            success_msg = font.render("Puzzle Résolu !", True, get_difficulty_color(difficulty_name) if difficulty_name else (0, 255, 0))
            success_rect = success_msg.get_rect(center=(screen.get_width() // 2, 50))
            screen.blit(success_msg, success_rect)
            
        elif frame < 180:
            # Phase 2: Message de félicitations stable
            screen.fill((40, 40, 40))
            
            # Dessiner le puzzle complet
            puzzle_x, puzzle_y, puzzle_width, puzzle_height = puzzle_area
            pygame.draw.rect(screen, (200, 200, 200), (puzzle_x-2, puzzle_y-2, puzzle_width+4, puzzle_height+4), 2)
            
            tile_width = puzzle_width // grid_size
            tile_height = puzzle_height // grid_size
            
            for i, tile in enumerate(tiles):
                row = i // grid_size
                col = i % grid_size
                x = puzzle_x + col * tile_width
                y = puzzle_y + row * tile_height
                screen.blit(pygame.transform.scale(tile, (tile_width, tile_height)), (x, y))
            
            success_msg = font.render("Félicitations !", True, get_difficulty_color(difficulty_name) if difficulty_name else (0, 255, 0))
            success_rect = success_msg.get_rect(center=(screen.get_width() // 2, 50))
            screen.blit(success_msg, success_rect)
            
        else:
            # Phase 3: Attendre l'input de l'utilisateur
            waiting_for_input = True
            screen.fill((40, 40, 40))
            
            # Dessiner le puzzle final
            puzzle_x, puzzle_y, puzzle_width, puzzle_height = puzzle_area
            pygame.draw.rect(screen, (200, 200, 200), (puzzle_x-2, puzzle_y-2, puzzle_width+4, puzzle_height+4), 2)
            
            tile_width = puzzle_width // grid_size
            tile_height = puzzle_height // grid_size
            
            for i, tile in enumerate(tiles):
                row = i // grid_size
                col = i % grid_size
                x = puzzle_x + col * tile_width
                y = puzzle_y + row * tile_height
                screen.blit(pygame.transform.scale(tile, (tile_width, tile_height)), (x, y))
            
            continue_msg = pygame.font.Font(None, 32).render("Appuyez sur une touche pour continuer...", True, (200, 200, 200))
            continue_rect = continue_msg.get_rect(center=(screen.get_width() // 2, screen.get_height() - 50))
            screen.blit(continue_msg, continue_rect)
        
        # Vérifier les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN and waiting_for_input:
                return
        
        pygame.display.flip()
        clock.tick(60)
        frame += 1

def game_loop(screen, image_path, grid_size, difficulty_name=None, level_index=None):
    # S'adapter à la taille de l'écran actuel
    SCREEN_WIDTH = screen.get_width()
    SCREEN_HEIGHT = screen.get_height()
    
    # Calculer les dimensions optimales pour le puzzle selon la difficulté
    if grid_size <= 4:  # Facile
        BASE_IMAGE_WIDTH = min(650, SCREEN_WIDTH - 500)
        BASE_IMAGE_HEIGHT = min(550, SCREEN_HEIGHT - 100)
    elif grid_size <= 8:  # Moyen
        BASE_IMAGE_WIDTH = min(800, SCREEN_WIDTH - 600)
        BASE_IMAGE_HEIGHT = min(700, SCREEN_HEIGHT - 100)
    elif grid_size <= 15:  # Difficile
        BASE_IMAGE_WIDTH = min(1000, SCREEN_WIDTH - 600)
        BASE_IMAGE_HEIGHT = min(800, SCREEN_HEIGHT - 100)
    else:  # Impossible
        BASE_IMAGE_WIDTH = min(1200, SCREEN_WIDTH - 600)
        BASE_IMAGE_HEIGHT = min(900, SCREEN_HEIGHT - 100)
    
    # Calculer les zones latérales proportionnellement
    SIDE_WIDTH = (SCREEN_WIDTH - BASE_IMAGE_WIDTH) // 2
    
    PUZZLE_X = SIDE_WIDTH
    PUZZLE_Y = (SCREEN_HEIGHT - BASE_IMAGE_HEIGHT) // 2  # Centrer verticalement
    
    # L'image utilise toute la largeur et hauteur de base
    PUZZLE_WIDTH = BASE_IMAGE_WIDTH
    PUZZLE_HEIGHT = BASE_IMAGE_HEIGHT
    
    # Calculer la taille des pièces
    TILE_WIDTH = PUZZLE_WIDTH // grid_size
    TILE_HEIGHT = PUZZLE_HEIGHT // grid_size
    
    # S'assurer que le puzzle reste dans les bonnes proportions
    if TILE_WIDTH * grid_size > PUZZLE_WIDTH or TILE_HEIGHT * grid_size > PUZZLE_HEIGHT:
        # Réajuster pour que tout rentre
        max_tile_width = PUZZLE_WIDTH // grid_size
        max_tile_height = PUZZLE_HEIGHT // grid_size
        TILE_WIDTH = min(max_tile_width, max_tile_height)
        TILE_HEIGHT = TILE_WIDTH  # Garder les pièces carrées
    
    pygame.display.set_caption("Puzzle en cours...")

    # Charger l'image originale
    original_image = pygame.image.load(image_path)
    
    # Redimensionner l'image pour s'adapter à la zone de puzzle
    puzzle_image_width = TILE_WIDTH * grid_size
    puzzle_image_height = TILE_HEIGHT * grid_size
    original_image = pygame.transform.scale(original_image, (puzzle_image_width, puzzle_image_height))

    def split_image(image):
        """Découpe l'image en pièces de puzzle irrégulières qui s'emboîtent"""
        pieces = []
        
        # Générer la carte des connexions pour tout le puzzle
        connections = generate_puzzle_connections(grid_size)
        
        # Calculer le padding nécessaire (plus grand pour éviter la coupure)
        bump_radius = min(TILE_WIDTH, TILE_HEIGHT) // 6
        padding = bump_radius * 2  # Plus de padding pour éviter que les protubérances soient coupées
        extended_width = TILE_WIDTH + padding * 2
        extended_height = TILE_HEIGHT + padding * 2
        
        for row in range(grid_size):
            for col in range(grid_size):
                # Position de base dans l'image originale
                base_x = col * TILE_WIDTH
                base_y = row * TILE_HEIGHT
                
                # Créer une surface étendue qui contiendra toute la zone de la pièce
                extended_piece = pygame.Surface((extended_width, extended_height), pygame.SRCALPHA)
                extended_piece.fill((0, 0, 0, 0))  # Transparent
                
                # Calculer la zone étendue dans l'image originale
                extended_x = base_x - padding  
                extended_y = base_y - padding
                
                # S'assurer qu'on ne dépasse pas les limites de l'image originale
                source_x = max(0, extended_x)
                source_y = max(0, extended_y)
                source_width = min(extended_width, image.get_width() - source_x)
                source_height = min(extended_height, image.get_height() - source_y)
                
                # Calculer où placer cette portion dans la surface étendue
                dest_x = source_x - extended_x
                dest_y = source_y - extended_y
                
                # Extraire la portion complète de l'image originale
                if source_width > 0 and source_height > 0:
                    source_rect = pygame.Rect(source_x, source_y, source_width, source_height)
                    source_portion = image.subsurface(source_rect).copy()
                    extended_piece.blit(source_portion, (dest_x, dest_y))
                
                # Créer le masque avec les connexions
                mask = create_puzzle_piece_mask(extended_width, extended_height, TILE_WIDTH, TILE_HEIGHT, padding, row, col, connections)
                
                # Appliquer le masque pour créer la pièce finale
                final_piece = pygame.Surface((extended_width, extended_height), pygame.SRCALPHA)
                final_piece.fill((0, 0, 0, 0))
                
                # Appliquer le masque: copier seulement les pixels blancs du masque
                for x in range(extended_width):
                    for y in range(extended_height):
                        if x < mask.get_width() and y < mask.get_height():
                            mask_pixel = mask.get_at((x, y))
                            if mask_pixel[3] > 0:  # Si le masque n'est pas transparent
                                if x < extended_piece.get_width() and y < extended_piece.get_height():
                                    image_pixel = extended_piece.get_at((x, y))
                                    if image_pixel[3] > 0:  # Si l'image n'est pas transparente
                                        final_piece.set_at((x, y), image_pixel)
                
                pieces.append(final_piece)
        
        # Remettre une seed aléatoire pour le placement des pièces
        random.seed()
        return pieces

    puzzle_pieces = split_image(original_image)
    
    # Calculer la taille étendue des pièces (MÊME calcul que dans split_image)
    bump_radius = min(TILE_WIDTH, TILE_HEIGHT) // 6
    padding = bump_radius * 2  # MÊME formule que dans split_image
    extended_tile_size = max(TILE_WIDTH + padding * 2, TILE_HEIGHT + padding * 2)
    
    # Structure des pièces : [piece_index, x, y, placed]
    pieces = []
    
    # Placer aléatoirement les pièces dans les zones latérales
    for i in range(len(puzzle_pieces)):
        # Choisir aléatoirement le côté gauche ou droit
        if random.choice([True, False]):
            # Côté gauche
            x = random.randint(10, max(10, SIDE_WIDTH - extended_tile_size - 10))
        else:
            # Côté droit  
            x = random.randint(PUZZLE_X + puzzle_image_width + 10, 
                             max(PUZZLE_X + puzzle_image_width + 10, SCREEN_WIDTH - extended_tile_size - 10))
        
        y = random.randint(10, max(10, SCREEN_HEIGHT - extended_tile_size - 10))
        pieces.append({'index': i, 'x': x, 'y': y, 'placed': False, 'size': extended_tile_size, 'padding': padding})
    
    # Grille de placement (True = occupé, False = libre)
    placement_grid = [[False for _ in range(grid_size)] for _ in range(grid_size)]
    
    # Variables de jeu
    selected_piece = None
    dragging = False
    drag_offset = (0, 0)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 32)
    show_reference = False  # État d'affichage de l'image de référence
    help_button_pressed = False  # État du bouton "?" (enfoncé ou non)
    pause_requested = False  # Demande de pause pour la capturer après le rendu
    
    # Bouton "?" en haut à droite
    help_button_size = 40
    help_button_rect = pygame.Rect(SCREEN_WIDTH - help_button_size - 10, 10, help_button_size, help_button_size)
    
    # Chronomètre avec gestion des pauses
    start_ticks = pygame.time.get_ticks()
    pause_time = 0  # Temps total passé en pause
    puzzle_solved = False
    
    # Système pour les effets temporaires de placement
    recent_placements = {}  # {piece_index: timestamp}
    
    # Couleur de la difficulté pour les effets visuels
    difficulty_color = get_difficulty_color(difficulty_name) if difficulty_name else (100, 149, 237)
    
    # Créer la texture bois pour tout l'arrière-plan
    wood_texture = create_wood_texture(SCREEN_WIDTH, SCREEN_HEIGHT)
    
    while True:
        # Couleur de fond selon la difficulté mais complètement remplacée par le bois
        bg_color = tuple(min(255, c + 20) for c in difficulty_color) if difficulty_name else (40, 40, 40)
        
        # Dessiner la texture bois sur tout l'arrière-plan
        screen.blit(wood_texture, (0, 0))
        
        # Zone centrale (plateau de puzzle) - fond gris clair avec grille
        puzzle_area = (PUZZLE_X, PUZZLE_Y, puzzle_image_width, puzzle_image_height)
        pygame.draw.rect(screen, (200, 200, 200), puzzle_area)  # Gris clair
        
        # Dessiner la grille
        for row in range(grid_size + 1):
            y = PUZZLE_Y + row * TILE_HEIGHT
            pygame.draw.line(screen, (150, 150, 150), (PUZZLE_X, y), (PUZZLE_X + puzzle_image_width, y), 1)
        
        for col in range(grid_size + 1):
            x = PUZZLE_X + col * TILE_WIDTH
            pygame.draw.line(screen, (150, 150, 150), (x, PUZZLE_Y), (x, PUZZLE_Y + puzzle_image_height), 1)
        
        # Afficher l'image de référence complète seulement si le bouton "?" est enfoncé
        if help_button_pressed:
            # Afficher l'image complète avec transparence
            reference_image = original_image.copy()
            reference_image.set_alpha(150)
            screen.blit(reference_image, (PUZZLE_X, PUZZLE_Y))
        # Sinon, ne rien afficher (juste le fond vert foncé)
        
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Marquer qu'une pause est demandée (sera traitée après le rendu)
                    pause_requested = True
                elif event.key == pygame.K_F11:
                    # Quitter le plein écran (retour au menu)
                    return "menu"
                        
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                
                # Vérifier si le bouton "?" est cliqué
                if help_button_rect.collidepoint(mx, my):
                    help_button_pressed = True
                    continue
                
                # Chercher la pièce cliquée (en commençant par le dessus)
                for piece in reversed(pieces):
                    if not piece['placed']:
                        # Utiliser le masque de la pièce pour une détection précise
                        tile = puzzle_pieces[piece['index']]
                        piece_mask = pygame.mask.from_surface(tile)
                        
                        # Calculer la position relative du clic dans la pièce
                        relative_x = mx - piece['x']
                        relative_y = my - piece['y']
                        
                        # Vérifier si le clic est sur une partie non-transparente de la pièce
                        if (0 <= relative_x < tile.get_width() and 
                            0 <= relative_y < tile.get_height() and
                            piece_mask.get_at((relative_x, relative_y))):
                            selected_piece = piece
                            dragging = True
                            drag_offset = (mx - piece['x'], my - piece['y'])
                            break
                            
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                # Relâcher le bouton "?" si il était enfoncé
                if help_button_pressed:
                    help_button_pressed = False
                
                if dragging and selected_piece:
                    mx, my = pygame.mouse.get_pos()
                    
                    # Vérifier si la pièce est lâchée dans la zone de puzzle
                    if (PUZZLE_X <= mx <= PUZZLE_X + puzzle_image_width and 
                        PUZZLE_Y <= my <= PUZZLE_Y + puzzle_image_height):
                        
                        # Calculer la position dans la grille (avec offset pour le centrage)
                        padding = selected_piece['padding']
                        adjusted_mx = mx + padding
                        adjusted_my = my + padding
                        
                        # Vérifier si c'est la bonne position pour cette pièce
                        correct_row = selected_piece['index'] // grid_size
                        correct_col = selected_piece['index'] % grid_size
                        
                        # Tolérance de placement réduite pour plus de précision
                        tolerance = TILE_WIDTH // 4  # Réduit de //2 à //4 pour une zone plus petite et plus précise
                        target_x = PUZZLE_X + correct_col * TILE_WIDTH - padding
                        target_y = PUZZLE_Y + correct_row * TILE_HEIGHT - padding
                        
                        # Position du centre de la pièce déplacée
                        piece_center_x = mx - drag_offset[0] + extended_tile_size // 2
                        piece_center_y = my - drag_offset[1] + extended_tile_size // 2
                        
                        # Position du centre de l'emplacement cible
                        target_center_x = target_x + extended_tile_size // 2
                        target_center_y = target_y + extended_tile_size // 2
                        
                        if (abs(piece_center_x - target_center_x) < tolerance and 
                            abs(piece_center_y - target_center_y) < tolerance and
                            not placement_grid[correct_row][correct_col]):
                            
                            # Placement correct - verrouillage avec effet !
                            selected_piece['x'] = target_x
                            selected_piece['y'] = target_y
                            selected_piece['placed'] = True
                            placement_grid[correct_row][correct_col] = True
                            
                            # Ajouter l'effet temporaire de placement
                            recent_placements[selected_piece['index']] = pygame.time.get_ticks()
                            
                            # Effet visuel de verrouillage (optionnel)
                            print(f"Pièce {selected_piece['index']} verrouillée en position ({correct_row}, {correct_col}) !")
                
                dragging = False
                selected_piece = None
                
            elif event.type == pygame.MOUSEMOTION and dragging and selected_piece:
                mx, my = pygame.mouse.get_pos()
                selected_piece['x'] = mx - drag_offset[0]
                selected_piece['y'] = my - drag_offset[1]
        
        # Nettoyer les effets temporaires expirés (plus de 1 seconde)
        current_time_ms = pygame.time.get_ticks()
        expired_effects = [piece_idx for piece_idx, timestamp in recent_placements.items() 
                          if current_time_ms - timestamp > 1000]
        for piece_idx in expired_effects:
            del recent_placements[piece_idx]
        
        # Dessiner toutes les pièces
        for piece in pieces:
            tile = puzzle_pieces[piece['index']]
            
            # D'abord dessiner la pièce
            screen.blit(tile, (piece['x'], piece['y']))
            
            # Effet de surbrillance pour la pièce sélectionnée
            if piece == selected_piece:
                draw_piece_outline(screen, tile, piece['x'], piece['y'], difficulty_color, 3)
            
            # Effet temporaire pour les pièces récemment placées (1 seconde)
            if piece['index'] in recent_placements:
                draw_piece_outline(screen, tile, piece['x'], piece['y'], (0, 255, 0), 2)
        
        # Afficher le temps (en soustrayant le temps de pause)
        current_time = (pygame.time.get_ticks() - start_ticks - pause_time) // 1000
        time_text = font.render(f"Temps: {current_time}s", True, (255, 255, 255))
        screen.blit(time_text, (10, 10))
        
        # Afficher le nom de la difficulté
        if difficulty_name:
            diff_text = font.render(difficulty_name, True, difficulty_color)
            screen.blit(diff_text, (10, SCREEN_HEIGHT - 30))
        
        # Dessiner le bouton "?" en haut à droite
        button_color = (255, 215, 0) if help_button_pressed else (100, 149, 237)
        pygame.draw.rect(screen, button_color, help_button_rect, border_radius=5)
        pygame.draw.rect(screen, (255, 255, 255), help_button_rect, 2, border_radius=5)
        help_font = pygame.font.SysFont(None, 28, bold=True)
        help_text = help_font.render("?", True, (255, 255, 255))
        help_text_rect = help_text.get_rect(center=help_button_rect.center)
        screen.blit(help_text, help_text_rect)
        
        # Vérifier si le puzzle est terminé
        if all(piece['placed'] for piece in pieces):
            if not puzzle_solved:
                puzzle_solved = True
                final_time = current_time
                
                # Marquer le niveau comme terminé
                if difficulty_name and level_index is not None:
                    mark_level_completed(difficulty_name, level_index, final_time)
                
                # Lancer l'animation de célébration
                celebration_animation(screen, puzzle_pieces, grid_size, puzzle_area, difficulty_name)
                return "menu"
        
        # Traiter la demande de pause APRÈS avoir tout dessiné
        if pause_requested:
            pause_requested = False
            # Capturer l'état actuel du jeu pour l'arrière-plan flouté (avec toutes les pièces)
            current_screen = screen.copy()
            pause_start = pygame.time.get_ticks()
            pause_menu = PauseMenu(screen, current_screen)
            pause_action = pause_menu.run()
            # Calculer le temps passé en pause
            pause_time += pygame.time.get_ticks() - pause_start
            if pause_action == "menu":
                return "menu"
            elif pause_action == "quit":
                return "quit"
            elif pause_action == "abandon":
                return "menu"
        
        pygame.display.flip()
        clock.tick(60)