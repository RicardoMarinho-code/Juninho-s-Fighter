import pygame
from config import SCREEN_HEIGHT, SCREEN_WIDTH
from game import Game
from assets import load_assets

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Juninho's Fighter")

assets = load_assets()

game =Game(screen, assets)
game.run()