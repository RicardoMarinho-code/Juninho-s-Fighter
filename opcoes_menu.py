import pygame
from character_select import select_character
from config import SCREEN_WIDTH
from ui_components import (
    Button, TITLE_FONT, HUD_FONT, WHITE, GRAY, BLUE, LIGHT_BLUE, DARK_BLUE, GOLD
)
from map_select import select_map

def show_controls(screen):
    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill(GRAY)
        title = TITLE_FONT.render("Controles", True, WHITE)
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 80)))

        controls = [
            "Jogador 1:",
            "  A/D = mover   W = pular   E = bloquear   R = ataque 1   T= ataque 2",
            "",
            "Jogador 2:",
            "  B/M = mover   SPACE = pular   L = bloquear   O = ataque 1   P = ataque 2"
        ]
        for i, txt in enumerate(controls):
            line = HUD_FONT.render(txt, True, WHITE)
            screen.blit(line, (SCREEN_WIDTH//2 - line.get_width()//2, 180 + i*40))

        back_btn = Button("Voltar", SCREEN_WIDTH//2 - 100, 400, 200, 60, BLUE, LIGHT_BLUE, DARK_BLUE)
        mouse = pygame.mouse.get_pos()
        back_btn.check_hover(mouse)
        back_btn.draw(screen)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.hovered:
                    running = False
        clock.tick(60)

def show_opcoes_menu(screen, volume):
    clock = pygame.time.Clock()
    running = True
    dragging = False
    # Barra de volume
    bar_x, bar_y, bar_w, bar_h = SCREEN_WIDTH//2 - 150, 220, 300, 16
    handle_radius = 18

    control_btn = Button("Controles", SCREEN_WIDTH//2 - 100, 300, 200, 60, BLUE, LIGHT_BLUE, DARK_BLUE)
    back_btn = Button("Voltar", SCREEN_WIDTH//2 - 100, 380, 200, 60, BLUE, LIGHT_BLUE, DARK_BLUE)

    while running:
        screen.fill(GRAY)
        title = TITLE_FONT.render("Opcoes", True, WHITE)
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
        control_btn.check_hover(mouse)
        back_btn.check_hover(mouse)
        control_btn.draw(screen)
        back_btn.draw(screen)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (handle_x-handle_radius <= mouse[0] <= handle_x+handle_radius and
                    bar_y-handle_radius <= mouse[1] <= bar_y+bar_h+handle_radius):
                    dragging = True
                elif control_btn.hovered:
                    show_controls(screen)
                elif back_btn.hovered:
                    running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
            elif event.type == pygame.MOUSEMOTION and dragging:
                rel_x = min(max(mouse[0], bar_x), bar_x+bar_w)
                volume = (rel_x - bar_x) / bar_w
                pygame.mixer.music.set_volume(volume)
        clock.tick(60)
    return volume

def show_menu(screen, volume=1.0):
    clock = pygame.time.Clock()
    buttons = {
        "jogar": Button("Jogar", SCREEN_WIDTH//2 - 100, 250, 200, 60, BLUE, LIGHT_BLUE, DARK_BLUE),
        "opcoes": Button("Opções", SCREEN_WIDTH//2 - 100, 320, 200, 60, BLUE, LIGHT_BLUE, DARK_BLUE),
        "sair": Button("Sair", SCREEN_WIDTH//2 - 100, 390, 200, 60, BLUE, LIGHT_BLUE, DARK_BLUE)
    }

    while True:
        screen.fill(GRAY)
        title = TITLE_FONT.render("Menu Principal", True, WHITE)
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 100)))

        # Desenha os botões
        for btn in buttons.values():
            btn.draw(screen)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                for name, btn in buttons.items():
                    if btn.hovered:
                        btn.pressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse = pygame.mouse.get_pos()
                for name, btn in buttons.items():
                    if btn.pressed and btn.hovered:
                        if name == "jogar":
                            p1, p2 = select_character(screen)
                            selected_map = select_map(screen)
                            return ("jogar", p1, p2, selected_map)
                        elif name == "opcoes":
                            volume = show_opcoes_menu(screen, volume)
                        elif name == "sair":
                            pygame.quit()
                            exit()
                    btn.pressed = False
            elif event.type == pygame.MOUSEMOTION:
                mouse = pygame.mouse.get_pos()
                for btn in buttons.values():
                    btn.check_hover(mouse)

        clock.tick(60)