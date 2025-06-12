import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from ui_components import (
    Button, BUTTON_FONT, TITLE_FONT, HUD_FONT, WHITE, GRAY, BLUE, LIGHT_BLUE, DARK_BLUE, GOLD
)

def show_controls(screen):
    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill(GRAY)
        title = TITLE_FONT.render("Controles", True, WHITE)
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 80)))

        controls = [
            "Jogador 1:",
            "  A/D = mover   W = pular   S = bloquear   F = ataque 1   G = ataque 2",
            "",
            "Jogador 2:",
            "  ←/→ = mover   ↑ = pular   ↓ = bloquear   K = ataque 1   L = ataque 2"
        ]
        for i, txt in enumerate(controls):
            line = HUD_FONT.render(txt, True, WHITE)
            screen.blit(line, (SCREEN_WIDTH//2 - line.get_width()//2, 180 + i*40))

        voltar_btn = Button("Voltar", SCREEN_WIDTH//2 - 100, 400, 200, 60, BLUE, LIGHT_BLUE, DARK_BLUE)
        mouse = pygame.mouse.get_pos()
        voltar_btn.check_hover(mouse)
        voltar_btn.draw(screen)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if voltar_btn.hovered:
                    running = False
        clock.tick(60)

def show_opcoes_menu(screen, volume):
    clock = pygame.time.Clock()
    running = True
    dragging = False
    # Barra de volume
    bar_x, bar_y, bar_w, bar_h = SCREEN_WIDTH//2 - 150, 220, 300, 16
    handle_radius = 18

    controles_btn = Button("Controles", SCREEN_WIDTH//2 - 100, 300, 200, 60, BLUE, LIGHT_BLUE, DARK_BLUE)
    voltar_btn = Button("Voltar", SCREEN_WIDTH//2 - 100, 380, 200, 60, BLUE, LIGHT_BLUE, DARK_BLUE)

    while running:
        screen.fill(GRAY)
        title = TITLE_FONT.render("Opções", True, WHITE)
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 100)))

        # Barra de volume
        vol_text = HUD_FONT.render("Volume", True, WHITE)
        screen.blit(vol_text, (bar_x, bar_y - 40))
        pygame.draw.rect(screen, (80,80,80), (bar_x, bar_y, bar_w, bar_h), border_radius=8)
        pygame.draw.rect(screen, GOLD, (bar_x, bar_y, int(bar_w * volume), bar_h), border_radius=8)
        # Handle
        handle_x = int(bar_x + bar_w * volume)
        pygame.draw.circle(screen, BLUE, (handle_x, bar_y + bar_h//2), handle_radius)
        pygame.draw.circle(screen, GOLD, (handle_x, bar_y + bar_h//2), handle_radius, 3)

        # Botões
        mouse = pygame.mouse.get_pos()
        controles_btn.check_hover(mouse)
        voltar_btn.check_hover(mouse)
        controles_btn.draw(screen)
        voltar_btn.draw(screen)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (handle_x-handle_radius <= mouse[0] <= handle_x+handle_radius and
                    bar_y-handle_radius <= mouse[1] <= bar_y+bar_h+handle_radius):
                    dragging = True
                elif controles_btn.hovered:
                    show_controls(screen)
                elif voltar_btn.hovered:
                    running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
            elif event.type == pygame.MOUSEMOTION and dragging:
                rel_x = min(max(mouse[0], bar_x), bar_x+bar_w)
                volume = (rel_x - bar_x) / bar_w
                pygame.mixer.music.set_volume(volume)
        clock.tick(60)
    return volume