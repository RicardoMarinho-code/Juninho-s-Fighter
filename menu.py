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
GRAY = (50, 50, 50)

# Inicializa pygame.font
pygame.font.init()

# Use uma fonte personalizada se preferir
try:
    title_font = pygame.font.Font("assets/font/turok.ttf", 72)
    button_font = pygame.font.Font("assets/font/turok.ttf", 48)
except:
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
        color = self.press_color if self.pressed else (self.hover_color if self.hovered else self.color)
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        text_surf = button_font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)

def show_options_menu(screen):
    clock = pygame.time.Clock()
    dragging = False
    volume = pygame.mixer.music.get_volume()

    # Barra de volume
    bar_x = SCREEN_WIDTH // 2 - 100
    bar_y = 260
    bar_width = 200
    bar_height = 20
    handle_radius = 10

    # Botão de voltar
    back_btn = Button("Voltar", SCREEN_WIDTH // 2 - 100, 350, 240, 60, BLUE, LIGHT_BLUE, DARK_BLUE)

    while True:
        screen.fill(GRAY)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]

        # Título
        title = title_font.render("Opcoes", True, WHITE)
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 150)))

        # Texto do volume
        vol_text = button_font.render(f"Volume: {int(volume * 100)}%", True, WHITE)
        screen.blit(vol_text, vol_text.get_rect(center=(SCREEN_WIDTH // 2, 220)))

        # Área da barra
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, BLUE, (bar_x, bar_y, bar_width * volume, bar_height))

        # Posição do handle
        handle_x = int(bar_x + bar_width * volume)
        pygame.draw.circle(screen, LIGHT_BLUE, (handle_x, bar_y + bar_height // 2), handle_radius)

        # Interação do mouse
        if click:
            if (
                bar_x <= mouse[0] <= bar_x + bar_width
                and bar_y - 10 <= mouse[1] <= bar_y + bar_height + 10
            ):
                dragging = True
        else:
            dragging = False

        if dragging:
            # Atualiza o volume com base na posição do mouse
            relative_x = max(bar_x, min(mouse[0], bar_x + bar_width))
            volume = (relative_x - bar_x) / bar_width
            pygame.mixer.music.set_volume(volume)

        # Botão Voltar
        back_btn.check_hover(mouse)
        back_btn.draw(screen)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.hovered:
                    back_btn.pressed = True
            elif e.type == pygame.MOUSEBUTTONUP:
                if back_btn.pressed and back_btn.hovered:
                    return  # voltar ao menu principal
                back_btn.pressed = False

        pygame.display.flip()
        clock.tick(60)


def show_menu(screen):
    clock = pygame.time.Clock()
    angle = 0

    button_width = 200
    button_height = 60

    buttons = {
        "jogar": Button("Jogar", SCREEN_WIDTH//2 - 100, 220, button_width, button_height, BLUE, LIGHT_BLUE, DARK_BLUE),
        "campanha": Button("Campanha", SCREEN_WIDTH//2 - 100, 300, button_width, button_height, BLUE, LIGHT_BLUE, DARK_BLUE),
        "opcoes": Button("Opções", SCREEN_WIDTH//2 - 100, 380, button_width, button_height, BLUE, LIGHT_BLUE, DARK_BLUE),
        "sair": Button("Sair", SCREEN_WIDTH//2 - 100, 460, button_width, button_height, BLUE, LIGHT_BLUE, DARK_BLUE),
    }

    while True:
        screen.fill(BLACK)
        mouse = pygame.mouse.get_pos()

        angle += 0.05
        offset_y = math.sin(angle) * 10
        title = title_font.render("Juninho's Fighter", True, WHITE)
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 120 + offset_y)))

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
                            # Jogador 1 escolhe
                            from character_select import selecionar_personagem
                            p1 = selecionar_personagem(screen, "Jogador 1: Selecione seu personagem")
                            # Jogador 2 escolhe
                            p2 = selecionar_personagem(screen, "Jogador 2: Selecione seu personagem")
                            # Você pode passar p1 e p2 para o jogo depois
                            return ("jogar", p1, p2)
                        elif name == "campanha":
                            from character_select import selecionar_personagem
                            p1 = selecionar_personagem(screen, "Selecione seu personagem")
                            # Só um jogador escolhe, o outro pode ser um padrão ou bot
                            return ("campanha", p1)
                        elif name == "opcoes":
                            show_options_menu(screen)
                        elif name == "sair":
                            pygame.quit()
                            sys.exit()
                    btn.pressed = False

        pygame.display.flip()
        clock.tick(60)

