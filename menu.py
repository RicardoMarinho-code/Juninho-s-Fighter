# menu.py
import pygame
import sys
import math
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from character_select import selecionar_personagem, selecionar_personagem_campanha
from campaign_tower import mostrar_torre
from ui_components import (
    Button, TITLE_FONT,
    WHITE, BLUE, LIGHT_BLUE, DARK_BLUE
)
from opcoes_menu import show_opcoes_menu

def show_menu(screen, volume=1.0):
    pygame.mouse.set_visible(True)
    clock = pygame.time.Clock()

    # Caminho ajustado para o background
    bg_img = pygame.image.load("assets/imagens/background/aeroporto.jpeg").convert()
    bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Botões
    jogar_btn = Button("Jogar", SCREEN_WIDTH//2 - 120, 250, 240, 60, BLUE, LIGHT_BLUE, DARK_BLUE)
    campanha_btn = Button("Campanha", SCREEN_WIDTH//2 - 120, 330, 240, 60, BLUE, LIGHT_BLUE, DARK_BLUE)
    opcoes_btn = Button("Opções", SCREEN_WIDTH//2 - 120, 410, 240, 60, BLUE, LIGHT_BLUE, DARK_BLUE)
    sair_btn = Button("Sair", SCREEN_WIDTH//2 - 120, 490, 240, 60, BLUE, LIGHT_BLUE, DARK_BLUE)
    buttons = {
        "jogar": jogar_btn,
        "campanha": campanha_btn,
        "opcoes": opcoes_btn,
        "sair": sair_btn
    }

    t = 0  # tempo para animação

    while True:
        # --- BACKGROUND ---
        screen.blit(bg_img, (0, 0))

        mouse = pygame.mouse.get_pos()

        # --- TÍTULO ANIMADO ---
        t += clock.get_time() / 1000  # segundos
        amplitude = 18  # pixels de movimento
        base_y = 120
        offset = math.sin(t * 2) * amplitude  # velocidade e amplitude
        title = TITLE_FONT.render("Juninho's Fighter", True, WHITE)
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, int(base_y + offset))))

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
                            p1, p2 = selecionar_personagem(screen)
                            return ("jogar", p1, p2, volume)
                        elif name == "campanha":
                            p1 = selecionar_personagem_campanha(screen)
                            mostrar_torre(screen, fase_atual=1)
                            return ("campanha", p1, volume)
                        elif name == "opcoes":
                            volume = show_opcoes_menu(screen, volume)
                        elif name == "sair":
                            pygame.quit()
                            sys.exit()
                    btn.pressed = False

        pygame.display.flip()
        clock.tick(60)

