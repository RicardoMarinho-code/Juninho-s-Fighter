import pygame
from config import SCREEN_HEIGHT, SCREEN_WIDTH  # Importa dimensões da tela
from game import Game  # Classe principal do jogo
from assets import load_assets  # Importa a função que carrega os assets

# Inicializa todos os módulos do Pygame
pygame.init()

# Cria a janela do jogo com as dimensões definidas no config.py
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Define o título da janela
pygame.display.set_caption("Juninho's Fighter")

# Agora que a janela foi criada, podemos carregar imagens e fontes com segurança
assets = load_assets()

# Cria o objeto principal do jogo e passa a tela e os recursos carregados
game = Game(screen, assets)

# Inicia o loop principal do jogo
game.run()
