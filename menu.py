# menu.py
import pygame
import sys
import math
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from character_select import select_character
from ui_components import (
    Button, TITLE_FONT,
    WHITE, BLUE, LIGHT_BLUE, DARK_BLUE
)
from opcoes_menu import show_opcoes_menu

def show_menu(screen, volume=1.0):
    pygame.mouse.set_visible(True)
    clock = pygame.time.Clock()

    bg_img = pygame.image.load("assets/imagens/background/aeroporto.jpeg").convert()
    bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # --- PADRONIZAÇÃO DE ESPAÇAMENTO ---
    button_width = 240
    button_height = 60
    spacing = 30  # Espaço vertical entre botões
    base_y = 250  # Posição Y do primeiro botão

    # Calcula as posições Y dos botões
    play_y = base_y
    options_y = play_y + button_height + spacing
    exit_y = options_y + button_height + spacing

    play_btn = Button("Jogar", SCREEN_WIDTH//2 - button_width//2, play_y, button_width, button_height, BLUE, LIGHT_BLUE, DARK_BLUE)
    opcoes_btn = Button("Opcoes", SCREEN_WIDTH//2 - button_width//2, options_y, button_width, button_height, BLUE, LIGHT_BLUE, DARK_BLUE)
    exit_btn = Button("Sair", SCREEN_WIDTH//2 - button_width//2, exit_y, button_width, button_height, BLUE, LIGHT_BLUE, DARK_BLUE)
    buttons = {
        "jogar": play_btn,
        "opcoes": opcoes_btn,
        "sair": exit_btn
    }

    t = 0  # tempo para animação

    while True:
        # --- BACKGROUND ---
        screen.blit(bg_img, (0, 0))

        mouse = pygame.mouse.get_pos()

        # --- TÍTULO ANIMADO ---
        t += clock.get_time() / 1000  # segundos
        amplitude = 18  # pixels de movimento
        base_title_y = 120
        offset = math.sin(t * 2) * amplitude
        title = TITLE_FONT.render("Juninho's Fighter", True, WHITE)
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, int(base_title_y + offset))))

        for btn in buttons.values():
            btn.check_hover(mouse)
            btn.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for btn in buttons.values():
                    if btn.hovered:
                        btn.pressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                for name, btn in buttons.items():
                    if btn.pressed and btn.hovered:
                        if name == "jogar":
                            p1, p2 = select_character(screen)
                            return ("jogar", p1, p2, volume)
                        elif name == "opcoes":
                            volume = show_opcoes_menu(screen, volume)
                        elif name == "sair":
                            pygame.quit()
                            sys.exit()
                    btn.pressed = False

        pygame.display.flip()
        clock.tick(60)

