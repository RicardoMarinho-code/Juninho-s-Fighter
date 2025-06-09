import pygame
from config import WHITE, RED, YELLOW

def draw_text(text, font, color, x, y, surface):
    img = font.render(text, True, color)
    surface.blit(img, (x, y))

def draw_health_bar(health, x, y, surface):
    ratio = health / 100
    pygame.draw.rect(surface, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(surface, RED, (x, y, 400, 30))
    pygame.draw.rect(surface, YELLOW, (x, y, 400 * ratio, 30))

def draw_background(background, surface, width, height):
    scaled_background = pygame.transform.scale(background, (width, height))
    surface.blit(scaled_background, (0, 0))
