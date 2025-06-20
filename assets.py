import pygame
from pygame import mixer

# Função que carrega todos os recursos (imagens, sons, fontes)
# Essa função só deve ser chamada após inicializar o display (pygame.display.set_mode)
def load_assets(selected_map):
    try:
        # Inicializa o mixer de áudio
        mixer.init()

        # Carrega música de fundo e define o volume
        # Corrija o nome do arquivo de música:
        pygame.mixer.music.load("assets/audio/WhatsApp-Audio-2025-05-29-at-15.05.08.mp3")
        pygame.mixer.music.set_volume(0.01)

        # Carrega efeitos sonoros
        sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
        sword_fx.set_volume(0.01)
        magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
        magic_fx.set_volume(0.01)# aumenta o volume do efeito sonoro de magia depois de testar

        # Carrega imagens com transparência (convert_alpha)
        # Só pode ser feito depois de iniciar a janela do Pygame
        assets = {}
        assets['background_img'] = pygame.image.load(selected_map).convert()
        assets['victory_img'] = pygame.image.load("assets/imagens/icons/victory.png").convert_alpha()
        assets['warrior_sheet'] = pygame.image.load("assets/imagens/warrior/sprites/warrior.png").convert_alpha()
        assets['wizard_sheet'] = pygame.image.load("assets/imagens/wizard/sprites/wizard.png").convert_alpha()
        assets['samurai_sheet'] = pygame.image.load("assets/imagens/Yasuke Samurai/Sprites/samurai.png").convert_alpha()
        assets['king_sheet'] = pygame.image.load("assets/imagens/king_yang/Sprites/yang.png").convert_alpha()

        # Carrega fontes com tamanho 80
        count_font = pygame.font.Font("assets/font/turok.ttf", 80)
        score_font = pygame.font.Font("assets/font/turok.ttf", 80)

        # Retorna todos os recursos organizados num dicionário
        return {
            "background_img": assets['background_img'],
            "victory_img": assets['victory_img'],
            "warrior_sheet": assets['warrior_sheet'],
            "wizard_sheet": assets['wizard_sheet'],
            "king_sheet": assets['king_sheet'],
            "samurai_sheet": assets['samurai_sheet'],
            "sword_fx": sword_fx,
            "magic_fx": magic_fx,
            "count_font": count_font,
            "score_font": score_font,
        }
    except Exception as e:
        print(f"Erro ao carregar assets: {e}")
        return {}
