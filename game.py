# game.py - Loop principal do jogo e controle dos rounds
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from ui import draw_background, draw_health_bar
from characters.fighter import *
from characters.input_thread import *
from utils.constants import *
from pause_menu import show_pause_menu  # <- menu de pausa
import threading
import sys

# Tenta carregar as fontes personalizadas, se não conseguir, usa as padrões do sistema
try:
    timer_font = pygame.font.Font("assets/font/turok.ttf", 54)
    score_font = pygame.font.Font("assets/font/turok.ttf", 36)
    hud_font = pygame.font.Font("assets/font/turok.ttf", 32)
except:
    timer_font = pygame.font.SysFont('Arial', 54, bold=True)
    score_font = pygame.font.SysFont('Arial', 36, bold=True)
    hud_font = pygame.font.SysFont('Arial', 32)

class Game:
    def __init__(self, screen, assets, score, p1="warrior", p2="wizard", modo="jogar"):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.score = score  # Usa o placar passado pelo main.py
        self.round_over = False
        self.round_over_time = 0
        self.intro_count = 3  # Contagem regressiva antes do round
        self.last_count_update = pygame.time.get_ticks()

        self.assets = assets

        # Dados dos personagens (tamanho, escala, offset)
        self.WARRIOR_DATA = [162, 4, [72, 56]]
        self.WIZARD_DATA = [250, 3, [112, 107]]
        # Quantidade de frames de cada animação
        self.WARRIOR_ANIM = [10, 8, 1, 7, 7, 3, 7]
        self.WIZARD_ANIM = [8, 8, 1, 8, 8, 3, 7]

        self.p1_name = p1
        self.p2_name = p2
        self.modo = modo
        self.create_fighter = lambda player, char_name, x, y, flip: (
            Fighter(player, x, y, flip, self.WARRIOR_DATA, assets['warrior_sheet'], self.WARRIOR_ANIM, assets['sword_fx'])
            if char_name == "warrior" else
            Fighter(player, x, y, flip, self.WIZARD_DATA, assets['wizard_sheet'], self.WIZARD_ANIM, assets['magic_fx'])
        )

        # P1 sempre à esquerda, P2 à direita
        self.player_1 = self.create_fighter(1, self.p1_name, 200, 380, False)
        self.player_2 = self.create_fighter(2, self.p2_name, 700, 380, True)

        # Inicia a música de fundo
        pygame.mixer.music.play(-1, 0.0, 5000)

        # Threads de input para ambos jogadores
        self.cmd_lock = threading.Lock()
        self.cmd_p1 = {'left': False, 'right': False, 'jump': False, 'block': False, 'attack1': False, 'attack2': False}
        self.stop_event = threading.Event()
        self.input_thread1 = InputThread(1, self.cmd_p1, self.stop_event, self.cmd_lock)
        self.input_thread1.start()
        self.cmd_p2 = {'left': False, 'right': False, 'jump': False, 'block': False, 'attack1': False, 'attack2': False}
        self.input_thread2 = InputThread(2, self.cmd_p2, self.stop_event, self.cmd_lock)
        self.input_thread2.start()

        self.round_time = 99  # time inicial do round em segundos
        self.last_timer_update = pygame.time.get_ticks()

    # Loop principal do jogo
    def run(self):
        run = True
        while run:
            self.clock.tick(FPS)

            # Desenha fundo, barras de vida e placar
            draw_background(self.assets['background_img'], self.screen, SCREEN_WIDTH, SCREEN_HEIGHT)
            # Barra de vida do P1 (esquerda)
            draw_health_bar(self.player_1.health, 20, 20, self.screen)
            # Barra de vida do P2 (direita)
            draw_health_bar(self.player_2.health, SCREEN_WIDTH - 416, 20, self.screen)

            # nome dos jogadores
            p1_name = "Jogador 1"
            p2_name = "Jogador 2"

            p1_label = hud_font.render(p1_name, True, (255,0,0))
            p2_label = hud_font.render(p2_name, True, (0,0,255))
            self.screen.blit(p1_label, (30, 60))
            self.screen.blit(p2_label, (SCREEN_WIDTH - p2_label.get_width() - 30, 60))

            # time centralizado entre as barras
            time_text = timer_font.render(str(self.round_time), True, (255, 215, 0))
            time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, 40))
            self.screen.blit(time_text, time_rect)

            # Placar centralizado abaixo do time
            score_text = score_font.render(f"{self.score[0]}  -  {self.score[1]}", True, (255,255,255))
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
            self.screen.blit(score_text, score_rect)

            # Se a contagem regressiva acabou, permite movimento dos jogadores
            if self.intro_count <= 0:
                with self.cmd_lock:
                    self.player_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, self.player_2, self.round_over, self.cmd_p1)
                    self.player_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, self.player_1, self.round_over, self.cmd_p2)
            else:
                # Exibe a contagem regressiva
                if self.intro_count > 0:
                    count_text = str(self.intro_count)
                    font = self.assets['count_font']
                    text_surf = font.render(count_text, True, (255,215,0))
                    text_shadow = font.render(count_text, True, (0,0,0))
                    rect = text_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
                    self.screen.blit(text_shadow, rect.move(4,4))
                    self.screen.blit(text_surf, rect)
                    if pygame.time.get_ticks() - self.last_count_update >= 1000:
                        self.intro_count -= 1
                        self.last_count_update = pygame.time.get_ticks()

            # Atualiza o timer a cada segundo
            if pygame.time.get_ticks() - self.last_timer_update > 1000 and self.round_time > 0 and not self.round_over:
                self.round_time -= 1
                self.last_timer_update = pygame.time.get_ticks()

            # Atualiza e desenha os personagens
            self.player_1.update()
            self.player_2.update()
            self.player_1.draw(self.screen)
            self.player_2.draw(self.screen)

            # Verifica fim de round e atualiza placar
            if not self.round_over:
                if not self.player_1.alive:
                    self.score[1] += 1
                    self.round_over = True
                    self.round_over_time = pygame.time.get_ticks()
                elif not self.player_2.alive:
                    self.score[0] += 1
                    self.round_over = True
                    self.round_over_time = pygame.time.get_ticks()
            else:
                # Exibe imagem de vitória e reinicia round após cooldown
                self.screen.blit(self.assets['victory_img'], (360, 150))
                if pygame.time.get_ticks() - self.round_over_time > ROUND_OVER_COOLDOWN:
                    self.round_over = False
                    self.intro_count = 3
                    self.player_1 = self.create_fighter(1, self.p1_name, 200, 380, False)
                    self.player_2 = self.create_fighter(2, self.p2_name, 700, 380, True)

            # --- ADICIONE ESTA VERIFICAÇÃO ---
            if self.score[0] == 2 or self.score[1] == 2:
                run = False
            # Trata eventos do sistema e pausa
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pause_result = show_pause_menu(self.screen)
                        if pause_result == "menu":
                            return "menu"

            pygame.display.update()
        
        # Finaliza as threads de input ao sair do loop
        self.stop_event.set()
        if hasattr(self, "input_thread1"):
            self.input_thread1.join()
        if hasattr(self, "input_thread2"):
            self.input_thread2.join()
        # NÃO chame pygame.quit() aqui!


