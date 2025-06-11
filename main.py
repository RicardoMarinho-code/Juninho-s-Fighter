# main.py
import pygame
import threading
from config import SCREEN_HEIGHT, SCREEN_WIDTH
from game import Game
from assets import load_assets
from menu import show_menu  # novo menu

# Inicializa o Pygame
pygame.init()
# Cria a janela do jogo com as dimensões definidas no config.py
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Juninho's Fighter")

# Exibe o menu inicial e só continua se o jogador clicar em "Jogar"
if show_menu(screen):
    assets = {}

    # Função para carregar os assets em uma thread separada
    def load_assets_thread():
        global assets
        assets = load_assets()

    # Inicia a thread de carregamento dos assets
    thread = threading.Thread(target=load_assets_thread)
    thread.start()

    # Fonte para exibir a mensagem de carregamento
    font = pygame.font.SysFont(None, 60)
    loading = True
    # Loop de carregamento: exibe "Carregando..." até os assets terminarem de carregar
    while loading:
        screen.fill((0, 0, 0))  # Preenche a tela de preto
        text = font.render("Carregando...", True, (255, 255, 255))
        # Centraliza o texto na tela
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
        pygame.display.update()
        # Verifica se a thread terminou de carregar os assets
        if not thread.is_alive():
            loading = False
        # Permite fechar a janela durante o carregamento
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    # Cria a instância do jogo passando a tela e os assets carregados
    game = Game(screen, assets)
    # Inicia o loop principal do jogo
    game.run()
