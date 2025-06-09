# ui.py - Funções para desenhar texto, barra de vida e fundo
import pygame
from config import WHITE, RED, YELLOW

def draw_text(text, font, color, x, y, surface):
    # Renderiza o texto e o desenha na tela
    img = font.render(text, True, color)
    surface.blit(img, (x, y))

def draw_health_bar(health, x, y, surface):
    # Desenha a barra de vida baseada na porcentagem de vida restante
    ratio = health / 100
    pygame.draw.rect(surface, WHITE, (x - 2, y - 2, 404, 34))  # Borda
    pygame.draw.rect(surface, RED, (x, y, 400, 30))  # Barra cheia
    pygame.draw.rect(surface, YELLOW, (x, y, 400 * ratio, 30))  # Barra atual

def draw_background(background, surface, width, height):
    # Redimensiona e desenha o fundo na tela
    scaled_background = pygame.transform.scale(background, (width, height))
    surface.blit(scaled_background, (0, 0))
