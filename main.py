import pygame
from config import SCREEN_HEIGHT, SCREEN_WIDTH
from game import Game
from assets import background_img, victory_img, warrior_sheet, wizard_sheet, sword_fx, magic_fx, count_font, score_font
pygame.init()
pygame.display.set_caption("Juninho's Fighter")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


assets = {
    "background_img": background_img,
    "victory_img": victory_img,
    "warrior_sheet": warrior_sheet,
    "wizard_sheet": wizard_sheet,
    "sword_fx": sword_fx,
    "magic_fx": magic_fx,
    "count_font": count_font,
    "score_font": score_font,
}

from game import Game
game = Game(screen, assets)
game.run()