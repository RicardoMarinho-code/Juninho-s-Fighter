# pause_menu.py
import pygame
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from ui_components import (
    Button, BUTTON_FONT, TITLE_FONT, WHITE, GRAY, BLUE, LIGHT_BLUE, DARK_BLUE
)
from opcoes_menu import show_opcoes_menu

def show_pause_menu(screen, stop_event=None, input_thread1=None, input_thread2=None, volume=1.0):
    clock = pygame.time.Clock()
    continue_btn = Button("Continuar", SCREEN_WIDTH//2 - 120, 230, 240, 60, BLUE, LIGHT_BLUE, DARK_BLUE)
    opcoes_btn = Button("Opções", SCREEN_WIDTH//2 - 120, 310, 240, 60, BLUE, LIGHT_BLUE, DARK_BLUE)
    menu_btn = Button("Menu Principal", SCREEN_WIDTH//2 - 160, 390, 320, 60, BLUE, LIGHT_BLUE, DARK_BLUE)  # Botão maior!
    buttons = [continue_btn, opcoes_btn, menu_btn]

    while True:
        screen.fill(GRAY)
        mouse_pos = pygame.mouse.get_pos()

        # Título
        title_surf = TITLE_FONT.render("PAUSADO", True, WHITE)
        screen.blit(title_surf, title_surf.get_rect(center=(SCREEN_WIDTH // 2, 160)))

        for btn in buttons:
            btn.check_hover(mouse_pos)
            btn.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for btn in buttons:
                    if btn.hovered:
                        btn.pressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                for btn in buttons:
                    if btn.pressed and btn.hovered:
                        if btn == continue_btn:
                            return "continue", volume
                        elif btn == opcoes_btn:
                            volume = show_opcoes_menu(screen, volume)
                        elif btn == menu_btn:
                            return "menu", volume
                    btn.pressed = False

        pygame.display.flip()
        clock.tick(60)
