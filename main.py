import pygame
import threading
from config import SCREEN_HEIGHT, SCREEN_WIDTH
from game import Game
from assets import load_assets

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Juninho's Fighter")

assets = {}

def load_assets_thread():
    global assets
    assets = load_assets()

# Inicia o carregamento dos assets em uma thread
thread = threading.Thread(target=load_assets_thread)
thread.start()

# Exibe tela de carregamento enquanto os assets são carregados
font = pygame.font.SysFont(None, 60)
loading = True
while loading:
    screen.fill((0, 0, 0))
    text = font.render("Carregando...", True, (255, 255, 255))
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()
    if not thread.is_alive():
        loading = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

game = Game(screen, assets)
game.run()