# character_select.py
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from ui_components import (
    TITLE_FONT, HUD_FONT, WHITE, GRAY, YELLOW
)

def select_character(screen):
    # Layout
    bar_width = 500
    bar_height = 110
    bar_x = (SCREEN_WIDTH - bar_width) // 2
    bar_y = SCREEN_HEIGHT // 2 + 40
    spacing = bar_width // 5  # 5 characters

    rect_width = spacing - 27
    rect_height = bar_height - 27

    # Load images
    warrior_img = pygame.image.load("assets/imagens/imgs_escolha/warrior_escolha.png").convert_alpha()
    wizard_img = pygame.image.load("assets/imagens/imgs_escolha/mage_escolha.png").convert_alpha()
    king_img = pygame.image.load("assets/imagens/imgs_escolha/king_escolha.png").convert_alpha()
    yasuke_img = pygame.image.load("assets/imagens/imgs_escolha/samurai_escolha.png").convert_alpha()
    warrior_frame = pygame.transform.smoothscale(warrior_img, (rect_width, rect_height))
    wizard_frame = pygame.transform.smoothscale(wizard_img, (rect_width, rect_height))
    king_frame = pygame.transform.smoothscale(king_img, (rect_width, rect_height))
    yasuke_frame = pygame.transform.smoothscale(yasuke_img, (rect_width, rect_height))

    names = ["Guerreiro", "Mago", "King", "Samurai", "???"]
    sprites = [warrior_frame, wizard_frame, king_frame, yasuke_frame, None]
    ids = ["warrior", "wizard", "king", "samurai", None]

    title_font = TITLE_FONT
    small_font = HUD_FONT

    selected = [None, None]  # [P1, P2]
    current = [0, 1]         # Current selection index for each player

    start_btn_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, bar_y + bar_height + 40, 200, 60)
    start_btn_hover = False

    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill(GRAY)
        # Title
        title = title_font.render("Character Selection", True, WHITE)
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 60)))

        # Player labels (above images, not overlapping)
        p1_label = small_font.render("Player 1", True, (255,0,0))
        p2_label = small_font.render("Player 2", True, (0,0,255))
        screen.blit(p1_label, (60, 120))
        screen.blit(p2_label, (SCREEN_WIDTH - p2_label.get_width() - 60, 120))

        # Show selected character images on the sides, below the labels
        sprite_width, sprite_height = 120, 240
        margin_x = 60
        image_y = 150  # below the label

        # P1 (left)
        if selected[0] is not None:
            idx = ids.index(selected[0])
            if sprites[idx]:
                img = pygame.transform.scale(sprites[idx], (sprite_width, sprite_height))
                img_rect = img.get_rect()
                img_rect.left = margin_x
                img_rect.top = image_y
                screen.blit(img, img_rect)
                # Outline for P1
                pygame.draw.rect(screen, (255, 0, 0), img_rect, 4, border_radius=12)

        # P2 (right)
        if selected[1] is not None:
            idx = ids.index(selected[1])
            if sprites[idx]:
                img = pygame.transform.scale(sprites[idx], (sprite_width, sprite_height))
                img_rect = img.get_rect()
                img_rect.right = SCREEN_WIDTH - margin_x
                img_rect.top = image_y
                screen.blit(img, img_rect)
                # Outline for P2
                pygame.draw.rect(screen, (0, 0, 255), img_rect, 4, border_radius=12)

        # Character selection bar
        for i, name in enumerate(names):
            rect = pygame.Rect(bar_x + i*spacing + 10, bar_y + 10, spacing-20, bar_height-20)
            # Current selection outline
            if current[0] == i:
                pygame.draw.rect(screen, (255, 0, 0), rect, 3, border_radius=10)
            if current[1] == i:
                pygame.draw.rect(screen, (0, 0, 255), rect, 3, border_radius=10)
            # Already chosen outline
            if selected[0] == ids[i]:
                pygame.draw.rect(screen, (255, 100, 100), rect, 5, border_radius=10)
            if selected[1] == ids[i]:
                pygame.draw.rect(screen, (100, 100, 255), rect, 5, border_radius=10)
            # Sprite or "?"

            if sprites[i]:
                img_rect = sprites[i].get_rect(center=rect.center)
                screen.blit(sprites[i], img_rect)
            else:
                lock_font = small_font
                lock = lock_font.render("?", True, (120,120,120))
                screen.blit(lock, lock.get_rect(center=rect.center))
            # Name
            name_surf = small_font.render(name, True, YELLOW)
            screen.blit(name_surf, name_surf.get_rect(center=(rect.centerx, rect.bottom + 18)))

        # Start button
        mouse = pygame.mouse.get_pos()
        start_btn_hover = start_btn_rect.collidepoint(mouse)
        btn_color = (0, 150, 255) if start_btn_hover and selected[0] and selected[1] else (0, 100, 200)
        pygame.draw.rect(screen, btn_color, start_btn_rect, border_radius=14)
        btn_text = title_font.render("START", True, WHITE if selected[0] and selected[1] else (180,180,180))
        btn_rect = btn_text.get_rect(center=start_btn_rect.center)
        screen.blit(btn_text, btn_rect)

        # Instructions (logo abaixo da barra)
        instr1 = small_font.render("Player 1: A/D to move, W to select", True, (255,0,0))
        instr2 = small_font.render("Player 2: B/M to move, SPACE to select", True, (0,0,255))
        instr_y = bar_y + bar_height + 110
        screen.blit(instr1, (bar_x, instr_y))
        screen.blit(instr2, (bar_x, instr_y + 30))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                import sys
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Player 1: A/D to move, W to select
                if event.key == pygame.K_a:
                    current[0] = (current[0] - 1) % len(names)
                elif event.key == pygame.K_d:
                    current[0] = (current[0] + 1) % len(names)
                elif event.key == pygame.K_w and ids[current[0]] is not None:
                    selected[0] = ids[current[0]]
                # Player 2: B/M to move, SPACE to select
                elif event.key == pygame.K_b:
                    current[1] = (current[1] - 1) % len(names)
                elif event.key == pygame.K_m:
                    current[1] = (current[1] + 1) % len(names)
                elif event.key == pygame.K_SPACE and ids[current[1]] is not None:
                    selected[1] = ids[current[1]]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn_hover and selected[0] and selected[1]:
                    running = False

        clock.tick(60)

    return selected[0], selected[1]

def select_ampaign_character(screen):
    warrior_img = pygame.image.load("assets/imagens/warrior/sprites/warrior.png").convert_alpha()
    wizard_img = pygame.image.load("assets/imagens/wizard/sprites/wizard.png").convert_alpha()
    warrior_frame = pygame.transform.scale(warrior_img.subsurface((0, 0, 80, 180)), (60, 120))
    wizard_frame = pygame.transform.scale(wizard_img.subsurface((0, 0, 80, 180)), (60, 120))

    names = ["Guerreiro", "Mago"]
    sprites = [warrior_frame, wizard_frame]
    ids = ["warrior", "wizard"]

    font = pygame.font.SysFont('Arial', 36)
    small_font = pygame.font.SysFont('Arial', 28)

    selected = None
    current = 0

    start_btn_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 100, 200, 60)
    start_btn_hover = False

    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill((30, 30, 30))
        title = font.render("Selecione seu personagem", True, WHITE)
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 100)))

        # Barra de seleção
        bar_width = 300
        bar_height = 110
        bar_x = (SCREEN_WIDTH - bar_width) // 2
        bar_y = SCREEN_HEIGHT // 2 - 40
        spacing = bar_width // len(names)
        for i, nome in enumerate(names):
            rect = pygame.Rect(bar_x + i*spacing + 10, bar_y + 10, spacing-20, bar_height-20)
            pygame.draw.rect(screen, (255, 0, 0) if current == i else (80, 80, 80), rect, 3, border_radius=10)
            if sprites[i]:
                img_rect = sprites[i].get_rect(center=rect.center)
                screen.blit(sprites[i], img_rect)
            name_surf = small_font.render(nome, True, YELLOW)
            screen.blit(name_surf, name_surf.get_rect(center=(rect.centerx, rect.bottom + 18)))

        # Botão iniciar
        mouse = pygame.mouse.get_pos()
        start_btn_hover = start_btn_rect.collidepoint(mouse)
        btn_color = (0, 150, 255) if start_btn_hover and selected else (0, 100, 200)
        pygame.draw.rect(screen, btn_color, start_btn_rect, border_radius=14)
        btn_text = font.render("INICIAR", True, WHITE if selected else (180,180,180))
        btn_rect = btn_text.get_rect(center=start_btn_rect.center)
        screen.blit(btn_text, btn_rect)

        instr = small_font.render("A/D para mover, W para escolher", True, (255,0,0))
        screen.blit(instr, (bar_x, bar_y - 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                import sys
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    current = (current - 1) % len(names)
                elif event.key == pygame.K_d:
                    current = (current + 1) % len(names)
                elif event.key == pygame.K_w:
                    selected = ids[current]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn_hover and selected:
                    running = False

        clock.tick(60)

    return selected
