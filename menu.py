# menu.py
import pygame
import math
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 150, 255)
LIGHT_BLUE = (100, 200, 255)
DARK_BLUE = (0, 100, 200)

# Fonte
pygame.font.init()
title_font = pygame.font.SysFont('Arial', 72)
button_font = pygame.font.SysFont('Arial', 48)

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
        current_color = self.press_color if self.pressed else (self.hover_color if self.hovered else self.color)
        pygame.draw.rect(surface, current_color, self.rect, border_radius=10)
        text_surface = button_font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

def show_menu(screen):
    clock = pygame.time.Clock()
    angle = 0

    # Botões
    button_width = 200
    button_height = 60
    buttons = {
        "jogar": Button("Jogar", SCREEN_WIDTH//2 - 100, 260, button_width, button_height, BLUE, LIGHT_BLUE, DARK_BLUE),
        "sair": Button("Sair", SCREEN_WIDTH//2 - 100, 360, button_width, button_height, BLUE, LIGHT_BLUE, DARK_BLUE),
    }

    running = True
    while running:
        screen.fill(BLACK)
        mouse_pos = pygame.mouse.get_pos()

        # Título animado
        angle += 0.05
        offset_y = math.sin(angle) * 10
        title_surface = title_font.render("Juninho's Fighter", True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 120 + offset_y))
        screen.blit(title_surface, title_rect)

        # Atualiza e desenha botões
        for btn in buttons.values():
            btn.check_hover(mouse_pos)
            btn.draw(screen)

        # Eventos
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
                            return True  # Inicia o jogo
                        elif name == "sair":
                            pygame.quit()
                            sys.exit()
                    btn.pressed = False

        pygame.display.flip()
        clock.tick(60)

    return False
