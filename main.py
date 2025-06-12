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
while True:
    menu_result = show_menu(screen)
    if not menu_result:
        break

    if isinstance(menu_result, tuple):
        modo = menu_result[0]
        if modo == "jogar":
            p1, p2 = menu_result[1], menu_result[2]
        elif modo == "campanha":
            p1 = menu_result[1]
            p2 = "wizard"  # Oponente da primeira fase

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

    # Sistema de melhor de três
    score = [0, 0]
    vencedor = None
    game = None  # Adicione esta linha para manter referência ao último game criado

    while True:
        if modo == "jogar":
            game = Game(screen, assets, score, p1, p2, modo)
        elif modo == "campanha":
            game = Game(screen, assets, score, p1, p2, modo)
        else:
            game = Game(screen, assets, score)
        resultado = game.run()
        if resultado == "menu":
            # Finaliza as threads antes de voltar ao menu
            if game:
                game.stop_event.set()
                game.input_thread1.join()
                game.input_thread2.join()
            break
        score = game.score
        if score[0] == 2 or score[1] == 2:
            vencedor = "Jogador 1" if score[0] == 2 else "Jogador 2"
            # Finaliza as threads antes de mostrar a tela de vitória
            if game:
                game.stop_event.set()
                game.input_thread1.join()
                game.input_thread2.join()
            break

    # Exibe tela de vitória final e espera ENTER
    waiting = True
    while waiting:
        screen.fill((0, 0, 0))
        win_text = font.render(f"{vencedor} venceu!", True, (255, 255, 0))
        info_text = font.render("Pressione ENTER para voltar ao menu", True, (255, 255, 255))
        screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 2 - win_text.get_height()))
        screen.blit(info_text, (SCREEN_WIDTH // 2 - info_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Finaliza as threads antes de sair do programa
                if game:
                    game.stop_event.set()
                    game.input_thread1.join()
                    game.input_thread2.join()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False
