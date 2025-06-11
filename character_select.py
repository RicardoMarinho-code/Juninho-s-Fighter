# character_select.py
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (30, 30, 30)
YELLOW = (255, 255, 0)
BORDER = (200, 0, 0)

pygame.font.init()
try:
    font = pygame.font.Font("assets/font/turok.ttf", 48)
except:
    font = pygame.font.SysFont('Arial', 48)

def selecionar_personagem(screen, titulo_jogador="Selecione seu personagem"):
    import pygame
    from config import SCREEN_WIDTH, SCREEN_HEIGHT
    # Carregue as sprites (um frame de cada personagem)
    warrior_img = pygame.image.load("assets/imagens/warrior/sprites/warrior.png").convert_alpha()
    wizard_img = pygame.image.load("assets/imagens/wizard/sprites/wizard.png").convert_alpha()
    # Ajuste o recorte se necessário (exemplo: pega só o primeiro frame)
    warrior_frame = warrior_img.subsurface((0, 0, 80, 180))
    wizard_frame = wizard_img.subsurface((0, 0, 80, 180))

    clock = pygame.time.Clock()
    # 5 espaços para personagens (2 implementados, 3 futuros)
    rects = [
        pygame.Rect(SCREEN_WIDTH // 6 - 75, 250, 150, 200),   # Espaço 1
        pygame.Rect(SCREEN_WIDTH * 2 // 6 - 75, 250, 150, 200), # Espaço 2
        pygame.Rect(SCREEN_WIDTH * 3 // 6 - 75, 250, 150, 200), # Espaço 3
        pygame.Rect(SCREEN_WIDTH * 4 // 6 - 75, 250, 150, 200), # Espaço 4
        pygame.Rect(SCREEN_WIDTH * 5 // 6 - 75, 250, 150, 200), # Espaço 5
    ]
    nomes = ["Guerreiro", "Mago", "???", "???", "???"]
    cores = [(180,0,0), (0,0,180), (80,80,80), (80,80,80), (80,80,80)]
    bordas = [ (200,0,0), (0,0,200), (100,100,100), (100,100,100), (100,100,100)]
    ids = ["warrior", "wizard", None, None, None]

    while True:
        screen.fill((30,30,30))
        titulo = font.render(titulo_jogador, True, WHITE)
        screen.blit(titulo, titulo.get_rect(center=(SCREEN_WIDTH // 2, 120)))

        for i, rect in enumerate(rects):
            pygame.draw.rect(screen, bordas[i], rect, border_radius=10)
            pygame.draw.rect(screen, cores[i], rect)
            nome_text = font.render(nomes[i], True, YELLOW)
            screen.blit(nome_text, nome_text.get_rect(center=(rect.centerx, rect.top - 40)))
            # Centraliza a sprite dentro do retângulo
            if ids[i] == "warrior":
                img = pygame.transform.scale(warrior_frame, (rect.width, rect.height))
                img_rect = img.get_rect(center=rect.center)
                screen.blit(img, img_rect)
            elif ids[i] == "wizard":
                img = pygame.transform.scale(wizard_frame, (rect.width, rect.height))
                img_rect = img.get_rect(center=rect.center)
                screen.blit(img, img_rect)
            elif ids[i] is None:
                # Desenha um cadeado simples (círculo + retângulo)
                lock_color = (120, 120, 120)
                pygame.draw.circle(screen, lock_color, rect.center, 30)
                pygame.draw.rect(screen, lock_color, (rect.centerx - 20, rect.centery, 40, 40), border_radius=8)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(rects):
                    if rect.collidepoint(event.pos) and ids[i] is not None:
                        return ids[i]

        pygame.display.flip()
        clock.tick(60)
