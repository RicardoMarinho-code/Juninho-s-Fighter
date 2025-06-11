# pause_menu.py
import pygame
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from menu import show_menu  # Importa o menu principal

# Cores
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
BLUE = (0, 150, 255)
LIGHT_BLUE = (100, 200, 255)
DARK_BLUE = (0, 100, 200)

# Fonte
pygame.font.init()
try:
    button_font = pygame.font.Font("assets/font/turok.ttf", 48)
    title_font = pygame.font.Font("assets/font/turok.ttf", 60)
except:
    button_font = pygame.font.SysFont('Arial', 48)
    title_font = pygame.font.SysFont('Arial', 60)

class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, press_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.press_color = press_color
        self.hovered = False
        self.pressed = False

    def draw(self, surface):
        color = self.press_color if self.pressed else (self.hover_color if self.hovered else self.color)
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        text_surf = button_font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)

def show_pause_menu(screen, stop_event=None, input_thread1=None, input_thread2=None):
    clock = pygame.time.Clock()

    continue_btn = Button("Continuar", SCREEN_WIDTH//2 - 100, 240, 240, 60, BLUE, LIGHT_BLUE, DARK_BLUE)
    menu_btn = Button("Menu Principal", SCREEN_WIDTH//2 - 100, 320, 240, 60, BLUE, LIGHT_BLUE, DARK_BLUE)
    # Removido o quit_btn

    while True:
        screen.fill(GRAY)
        mouse_pos = pygame.mouse.get_pos()

        # Título
        title_surf = title_font.render("PAUSADO", True, WHITE)
        screen.blit(title_surf, title_surf.get_rect(center=(SCREEN_WIDTH // 2, 140)))

        # Botões (apenas continuar e menu)
        for btn in [continue_btn, menu_btn]:
            btn.check_hover(mouse_pos)
            btn.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Apenas retorna para o menu principal, não fecha o jogo aqui
                return "menu"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for btn in [continue_btn, menu_btn]:
                    if btn.hovered:
                        btn.pressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                for btn in [continue_btn, menu_btn]:
                    if btn.pressed and btn.hovered:
                        if btn == continue_btn:
                            return "continue"
                        elif btn == menu_btn:
                            return "menu"
                    btn.pressed = False

        pygame.display.flip()
        clock.tick(60)
