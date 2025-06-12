import pygame

# Cores padronizadas
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
BLUE = (0, 150, 255)
LIGHT_BLUE = (100, 200, 255)
DARK_BLUE = (0, 100, 200)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)
RED = (255, 0, 0)

# Fontes padronizadas
pygame.font.init()
try:
    BUTTON_FONT = pygame.font.Font("assets/font/turok.ttf", 48)
    TITLE_FONT = pygame.font.Font("assets/font/turok.ttf", 60)
    HUD_FONT = pygame.font.Font("assets/font/turok.ttf", 32)
    TIMER_FONT = pygame.font.Font("assets/font/turok.ttf", 54)
    PLACAR_FONT = pygame.font.Font("assets/font/turok.ttf", 36)
except:
    BUTTON_FONT = pygame.font.SysFont('Arial', 48)
    TITLE_FONT = pygame.font.SysFont('Arial', 60)
    HUD_FONT = pygame.font.SysFont('Arial', 32)
    TIMER_FONT = pygame.font.SysFont('Arial', 54, bold=True)
    PLACAR_FONT = pygame.font.SysFont('Arial', 36, bold=True)

# Classe Button padronizada
class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, press_color, font=BUTTON_FONT):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.press_color = press_color
        self.hovered = False
        self.pressed = False
        self.font = font

    def draw(self, surface):
        # Sombra
        shadow_rect = self.rect.copy()
        shadow_rect.y += 4
        pygame.draw.rect(surface, (30,30,30), shadow_rect, border_radius=16)
        # Borda dourada
        pygame.draw.rect(surface, GOLD, self.rect, border_radius=16)
        # Botão principal
        color = self.press_color if self.pressed else (self.hover_color if self.hovered else self.color)
        pygame.draw.rect(surface, color, self.rect.inflate(-6, -6), border_radius=14)
        # Texto com sombra
        text_surf = self.font.render(self.text, True, WHITE)
        text_shadow = self.font.render(self.text, True, (0,0,0))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_shadow, text_rect.move(2,2))
        surface.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)