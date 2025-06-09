import pygame
from pygame import mixer
pygame.display.set_caption("Juninho's Fighter")
mixer.init()

# Sons
pygame.mixer.music.load("assets/audio/WhatsApp-Audio-2025-05-29-at-15.05.08.mp3")
pygame.mixer.music.set_volume(0.1)
sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.1)
magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
magic_fx.set_volume(0.25)

# Imagens
background_img = pygame.image.load("assets/imagens/Background/background1.jpeg").convert_alpha()
victory_img = pygame.image.load("assets/imagens/icons/victory.png").convert_alpha()

warrior_sheet = pygame.image.load("assets/imagens/warrior/sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/imagens/wizard/sprites/wizard.png").convert_alpha()

# Fontes
count_font = pygame.font.Font("assets/font/turok.ttf", 80)
score_font = pygame.font.Font("assets/font/turok.ttf", 80)
