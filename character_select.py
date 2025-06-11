# character_select.py
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (30, 30, 30)
YELLOW = (255, 255, 0)
BORDER = (200, 0, 0)

pygame.font.init()
try:
    font = pygame.font.Font("assets/font/turok.ttf", 48)
except:
    font = pygame.font.SysFont('Arial', 48)

def selecionar_personagem(screen, titulo_jogador="Selecione seu personagem"):
    clock = pygame.time.Clock()
    warrior_rect = pygame.Rect(SCREEN_WIDTH // 4 - 75, 250, 150, 200)
    wizard_rect = pygame.Rect(SCREEN_WIDTH * 3 // 4 - 75, 250, 150, 200)
    
    while True:
        screen.fill(GRAY)
        titulo = font.render(titulo_jogador, True, WHITE)
        screen.blit(titulo, titulo.get_rect(center=(SCREEN_WIDTH // 2, 120)))

        pygame.draw.rect(screen, BORDER, warrior_rect, border_radius=10)
        pygame.draw.rect(screen, BORDER, wizard_rect, border_radius=10)

        warrior_text = font.render("Guerreiro", True, YELLOW)
        screen.blit(warrior_text, warrior_text.get_rect(center=(warrior_rect.centerx, warrior_rect.top - 40)))

        wizard_text = font.render("Mago", True, YELLOW)
        screen.blit(wizard_text, wizard_text.get_rect(center=(wizard_rect.centerx, wizard_rect.top - 40)))

        pygame.draw.rect(screen, (180, 0, 0), warrior_rect)
        pygame.draw.rect(screen, (0, 0, 180), wizard_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if warrior_rect.collidepoint(event.pos):
                    return "warrior"
                elif wizard_rect.collidepoint(event.pos):
                    return "wizard"

        pygame.display.flip()
        clock.tick(60)
