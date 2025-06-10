# game.py - Loop principal do jogo e controle dos rounds
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from ui import draw_background, draw_health_bar, draw_text
from characters.fighter import *
from characters.input_thread import *
from utils.constants import *
from pause_menu import show_pause_menu  # <- menu de pausa
import threading

class Game:
    def __init__(self, screen, assets):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.score = [0, 0]
        self.round_over = False
        self.round_over_time = 0
        self.intro_count = 3
        self.last_count_update = pygame.time.get_ticks()

        self.assets = assets

        self.WARRIOR_DATA = [162, 4, [72, 56]]
        self.WIZARD_DATA = [250, 3, [112, 107]]
        self.WARRIOR_ANIM = [10, 8, 1, 7, 7, 3, 7]
        self.WIZARD_ANIM = [8, 8, 1, 8, 8, 3, 7]

        self.player_1 = Fighter(1, 200, 380, False, self.WARRIOR_DATA, assets['warrior_sheet'], self.WARRIOR_ANIM, assets['sword_fx'])
        self.player_2 = Fighter(2, 700, 380, True, self.WIZARD_DATA, assets['wizard_sheet'], self.WIZARD_ANIM, assets['magic_fx'])

        pygame.mixer.music.play(-1, 0.0, 5000)

        self.cmd_p1 = {'left': False, 'right': False, 'jump': False, 'block': False, 'attack1': False, 'attack2': False}
        self.cmd_p2 = {'left': False, 'right': False, 'jump': False, 'block': False, 'attack1': False, 'attack2': False}
        self.stop_event = threading.Event()
        self.input_thread1 = InputThread(1, self.cmd_p1, self.stop_event)
        self.input_thread2 = InputThread(2, self.cmd_p2, self.stop_event)
        self.input_thread1.start()
        self.input_thread2.start()

    def run(self):
        run = True
        while run:
            self.clock.tick(FPS)

            draw_background(self.assets['background_img'], self.screen, SCREEN_WIDTH, SCREEN_HEIGHT)
            draw_health_bar(self.player_1.health, 20, 20, self.screen)
            draw_health_bar(self.player_2.health, 580, 20, self.screen)
            draw_text("P1: " + str(self.score[0]), self.assets['score_font'], (255, 0, 0), 20, 60, self.screen)
            draw_text("P2: " + str(self.score[1]), self.assets['score_font'], (255, 0, 0), 580, 60, self.screen)

            if self.intro_count <= 0:
                self.player_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, self.player_2, self.round_over, self.cmd_p1)
                self.player_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, self.player_1, self.round_over, self.cmd_p2)
            else:
                draw_text(str(self.intro_count), self.assets['count_font'], (255, 0, 0),
                          SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3, self.screen)
                if pygame.time.get_ticks() - self.last_count_update >= 1000:
                    self.intro_count -= 1
                    self.last_count_update = pygame.time.get_ticks()

            self.player_1.update()
            self.player_2.update()
            self.player_1.draw(self.screen)
            self.player_2.draw(self.screen)

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
                self.screen.blit(self.assets['victory_img'], (360, 150))
                if pygame.time.get_ticks() - self.round_over_time > ROUND_OVER_COOLDOWN:
                    self.round_over = False
                    self.intro_count = 3
                    self.player_1 = Fighter(1, 200, 380, False, self.WARRIOR_DATA,
                                            self.assets['warrior_sheet'], self.WARRIOR_ANIM, self.assets['sword_fx'])
                    self.player_2 = Fighter(2, 700, 380, True, self.WIZARD_DATA,
                                            self.assets['wizard_sheet'], self.WIZARD_ANIM, self.assets['magic_fx'])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        show_pause_menu(self.screen)  # <- chama o menu de pausa

            pygame.display.update()
        
        self.stop_event.set()
        self.input_thread1.join()
        self.input_thread2.join()
        pygame.quit()
