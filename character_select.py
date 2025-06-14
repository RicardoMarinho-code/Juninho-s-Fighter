# character_select.py
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from ui_components import (
    TITLE_FONT, HUD_FONT, WHITE, GRAY, YELLOW
)

def selecionar_personagem(screen):
    import pygame
    from config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, YELLOW

    # Defina o tamanho do retângulo de seleçãotitulo_jogador
    bar_width = 500
    bar_height = 110
    bar_x = (SCREEN_WIDTH - bar_width) // 2
    bar_y = SCREEN_HEIGHT // 2 + 60
    spacing = bar_width // 5  # 5 personagens

    # Tamanho do retângulo interno (igual ao usado no loop de desenho)
    rect_width = spacing - 20
    rect_height = bar_height - 20

    # Carrega as imagens originais
    warrior_img = pygame.image.load("assets/imagens/imgs_escolha/warrior_escolha.png").convert_alpha()
    wizard_img = pygame.image.load("assets/imagens/imgs_escolha/mage_escolha.png").convert_alpha()

    # Redimensiona/comprime para caber no retângulo (sem cortar)
    warrior_frame = pygame.transform.smoothscale(warrior_img, (rect_width, rect_height))
    wizard_frame = pygame.transform.smoothscale(wizard_img, (rect_width, rect_height))

    nomes = ["Guerreiro", "Mago", "???", "???", "???"]
    sprites = [warrior_frame, wizard_frame, None, None, None]
    ids = ["warrior", "wizard", None, None, None]

    title_font = TITLE_FONT
    small_font = HUD_FONT

    selected = [None, None]  # [P1, P2]
    current = [0, 1]         # Índice atual de seleção para cada player

    start_btn_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, bar_y + bar_height + 40, 200, 60)
    start_btn_hover = False

    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill(GRAY)
        title = title_font.render("Seleção de Personagem", True, WHITE)
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 80)))

        # Nomes dos jogadores nos cantos
        p1_label = small_font.render("Jogador 1", True, (255,0,0))
        p2_label = small_font.render("Jogador 2", True, (0,0,255))
        screen.blit(p1_label, (40, 220))
        screen.blit(p2_label, (SCREEN_WIDTH - p2_label.get_width() - 40, 220))

        # Mostra personagem escolhido por cada player nos lados
        sprite_width, sprite_height = 120, 240
        margin_x = 60  # margem da borda da tela

        # P1 (esquerda) - centralizado verticalmente, afastado da borda
        if selected[0] is not None:
            idx = ids.index(selected[0])
            if sprites[idx]:
                img = pygame.transform.scale(sprites[idx], (sprite_width, sprite_height))
                img_rect = img.get_rect()
                img_rect.left = margin_x
                img_rect.centery = SCREEN_HEIGHT // 2
                screen.blit(img, img_rect)
                # Para P1
                pygame.draw.rect(screen, (0,255,0), img_rect, 2)

        # P2 (direita) - centralizado verticalmente, afastado da borda
        if selected[1] is not None:
            idx = ids.index(selected[1])
            if sprites[idx]:
                img = pygame.transform.scale(sprites[idx], (sprite_width, sprite_height))
                img_rect = img.get_rect()
                img_rect.right = SCREEN_WIDTH - margin_x
                img_rect.centery = SCREEN_HEIGHT // 2
                screen.blit(img, img_rect)
                # Para P2
                pygame.draw.rect(screen, (255,0,0), img_rect, 2)

        # Barra de seleção de personagens (sem borda dourada)
        spacing = bar_width // len(nomes)
        for i, nome in enumerate(nomes):
            rect = pygame.Rect(bar_x + i*spacing + 10, bar_y + 10, spacing-20, bar_height-20)
            # Borda de seleção atual (apenas colorida)
            if current[0] == i:
                pygame.draw.rect(screen, (255, 0, 0), rect, 3, border_radius=10)
            if current[1] == i:
                pygame.draw.rect(screen, (0, 0, 255), rect, 3, border_radius=10)
            # Borda de personagem já escolhido
            if selected[0] == ids[i]:
                pygame.draw.rect(screen, (255, 100, 100), rect, 5, border_radius=10)
            if selected[1] == ids[i]:
                pygame.draw.rect(screen, (100, 100, 255), rect, 5, border_radius=10)
            # Sprite ou "?"

            if sprites[i]:
                img_rect = sprites[i].get_rect(center=rect.center)
                screen.blit(sprites[i], img_rect)
            else:
                lock_font = pygame.font.SysFont('Arial', 40)
                lock = lock_font.render("?", True, (120,120,120))
                screen.blit(lock, lock.get_rect(center=rect.center))
            # Nome
            name_surf = small_font.render(nome, True, YELLOW)
            screen.blit(name_surf, name_surf.get_rect(center=(rect.centerx, rect.bottom + 18)))

        # Botão iniciar
        mouse = pygame.mouse.get_pos()
        start_btn_hover = start_btn_rect.collidepoint(mouse)
        btn_color = (0, 150, 255) if start_btn_hover and selected[0] and selected[1] else (0, 100, 200)
        pygame.draw.rect(screen, btn_color, start_btn_rect, border_radius=14)
        btn_text = title_font.render("INICIAR", True, WHITE if selected[0] and selected[1] else (180,180,180))
        btn_rect = btn_text.get_rect(center=start_btn_rect.center)
        screen.blit(btn_text, btn_rect)

        # Instruções
        instr1 = small_font.render("Jogador 1: A/D para mover, W para escolher", True, (255,0,0))
        instr2 = small_font.render("Jogador 2: ←/→ para mover, ↑ para escolher", True, (0,0,255))
        screen.blit(instr1, (bar_x, bar_y - 40))
        screen.blit(instr2, (bar_x, bar_y - 20))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                # Jogador 1: A/D para mover, W para selecionar
                if event.key == pygame.K_a:
                    current[0] = (current[0] - 1) % len(nomes)
                elif event.key == pygame.K_d:
                    current[0] = (current[0] + 1) % len(nomes)
                elif event.key == pygame.K_w and ids[current[0]] is not None:
                    selected[0] = ids[current[0]]
                # Jogador 2: ←/→ para mover, ↑ para selecionar
                elif event.key == pygame.K_LEFT:
                    current[1] = (current[1] - 1) % len(nomes)
                elif event.key == pygame.K_RIGHT:
                    current[1] = (current[1] + 1) % len(nomes)
                elif event.key == pygame.K_UP and ids[current[1]] is not None:
                    selected[1] = ids[current[1]]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn_hover and selected[0] and selected[1]:
                    running = False

        clock.tick(60)

    return selected[0], selected[1]

def selecionar_personagem_campanha(screen):
    warrior_img = pygame.image.load("assets/imagens/warrior/sprites/warrior.png").convert_alpha()
    wizard_img = pygame.image.load("assets/imagens/wizard/sprites/wizard.png").convert_alpha()
    warrior_frame = pygame.transform.scale(warrior_img.subsurface((0, 0, 80, 180)), (60, 120))
    wizard_frame = pygame.transform.scale(wizard_img.subsurface((0, 0, 80, 180)), (60, 120))

    nomes = ["Guerreiro", "Mago"]
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
        spacing = bar_width // len(nomes)
        for i, nome in enumerate(nomes):
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
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    current = (current - 1) % len(nomes)
                elif event.key == pygame.K_d:
                    current = (current + 1) % len(nomes)
                elif event.key == pygame.K_w:
                    selected = ids[current]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn_hover and selected:
                    running = False

        clock.tick(60)

    return selected
