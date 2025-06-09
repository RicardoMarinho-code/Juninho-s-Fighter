import pygame
from pygame import mixer

# Função que carrega todos os recursos (imagens, sons, fontes)
# Essa função só deve ser chamada após inicializar o display (pygame.display.set_mode)
def load_assets():
    # Inicializa o mixer de áudio
    mixer.init()

    # Carrega música de fundo e define o volume
    pygame.mixer.music.load("assets/audio/WhatsApp-Audio-2025-05-29-at-15.05.08.mp3")
    pygame.mixer.music.set_volume(0.1)

    # Carrega efeitos sonoros
    sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
    sword_fx.set_volume(0.1)
    magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
    magic_fx.set_volume(0.25)

    # Carrega imagens com transparência (convert_alpha)
    # Só pode ser feito depois de iniciar a janela do Pygame
    background_img = pygame.image.load("assets/imagens/Background/background1.jpeg").convert_alpha()
    victory_img = pygame.image.load("assets/imagens/icons/victory.png").convert_alpha()
    warrior_sheet = pygame.image.load("assets/imagens/warrior/sprites/warrior.png").convert_alpha()
    wizard_sheet = pygame.image.load("assets/imagens/wizard/sprites/wizard.png").convert_alpha()

    # Carrega fontes com tamanho 80
    count_font = pygame.font.Font("assets/font/turok.ttf", 80)
    score_font = pygame.font.Font("assets/font/turok.ttf", 80)

    # Retorna todos os recursos organizados num dicionário
    return {
        "background_img": background_img,
        "victory_img": victory_img,
        "warrior_sheet": warrior_sheet,
        "wizard_sheet": wizard_sheet,
        "sword_fx": sword_fx,
        "magic_fx": magic_fx,
        "count_font": count_font,
        "score_font": score_font,
    }
