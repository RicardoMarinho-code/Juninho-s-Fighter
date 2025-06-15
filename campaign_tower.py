import pygame
from config import SCREEN_WIDTH
from ui_components import (
    Button, TITLE_FONT, WHITE, GRAY, BLUE, LIGHT_BLUE, DARK_BLUE
)

def show_tower(screen, current_phase=1):
    font = TITLE_FONT
    phases = ["Fase 1: Mago", "Fase 2", "Fase 3", "Fase 4", "Fase 5", "Chefe"]
    tower_x = SCREEN_WIDTH // 2 - 60
    tower_y = 120
    Floor_height = 60

    go_btn = Button("GO!", SCREEN_WIDTH//2 - 80, tower_y + Floor_height*len(phases) + 40, 160, 50, BLUE, LIGHT_BLUE, DARK_BLUE)

    clock = pygame.time.Clock()
    waiting = True
    while waiting:
        screen.fill(GRAY)
        title = font.render("Torre do Desafio", True, WHITE)
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 60)))

        # Desenha a torre
        for i, name in enumerate(phases):
            rect = pygame.Rect(tower_x, tower_y + i*Floor_height, 120, Floor_height-8)
            collor = (255, 215, 0) if i == current_phase-1 else (80, 80, 80)
            pygame.draw.rect(screen, collor, rect, border_radius=10)
            text_phase = font.render(name, True, WHITE)
            screen.blit(text_phase, (rect.right + 20, rect.centery - text_phase.get_height()//2))

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