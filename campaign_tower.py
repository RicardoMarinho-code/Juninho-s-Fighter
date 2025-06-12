import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from ui_components import (
    Button, TITLE_FONT, WHITE, GRAY, BLUE, LIGHT_BLUE, DARK_BLUE
)

def mostrar_torre(screen, fase_atual=1):
    font = TITLE_FONT
    fases = ["Fase 1: Mago", "Fase 2", "Fase 3", "Fase 4", "Fase 5", "Chefe"]
    tower_x = SCREEN_WIDTH // 2 - 60
    tower_y = 120
    andar_altura = 60

    go_btn = Button("GO!", SCREEN_WIDTH//2 - 80, tower_y + andar_altura*len(fases) + 40, 160, 50, BLUE, LIGHT_BLUE, DARK_BLUE)

    clock = pygame.time.Clock()
    waiting = True
    while waiting:
        screen.fill(GRAY)
        title = font.render("Torre do Desafio", True, WHITE)
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 60)))

        # Desenha a torre
        for i, nome in enumerate(fases):
            rect = pygame.Rect(tower_x, tower_y + i*andar_altura, 120, andar_altura-8)
            cor = (255, 215, 0) if i == fase_atual-1 else (80, 80, 80)
            pygame.draw.rect(screen, cor, rect, border_radius=10)
            fase_text = font.render(nome, True, WHITE)
            screen.blit(fase_text, (rect.right + 20, rect.centery - fase_text.get_height()//2))

        mouse = pygame.mouse.get_pos()
        go_btn.check_hover(mouse)
        go_btn.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if go_btn.hovered:
                    waiting = False

        clock.tick(60)