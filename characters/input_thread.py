import threading
import pygame
import time

# Thread responsável por ler o teclado e atualizar os comandos do jogador
class InputThread(threading.Thread):
    def __init__(self, player, command_dict, stop_event, cmd_lock):
        super().__init__()
        self.player = player
        self.command_dict = command_dict
        self.stop_event = stop_event
        self.cmd_lock = cmd_lock

    def run(self):
        while not self.stop_event.is_set():
            key = pygame.key.get_pressed()
            # Usa lock para garantir acesso seguro ao dicionário de comandos
            with self.cmd_lock:
                if self.player == 1:
                    self.command_dict['left'] = key[pygame.K_a]
                    self.command_dict['right'] = key[pygame.K_d]
                    self.command_dict['jump'] = key[pygame.K_w]
                    self.command_dict['attack1'] = key[pygame.K_r]
                    self.command_dict['attack2'] = key[pygame.K_t]
                elif self.player == 2:
                    self.command_dict['left'] = key[pygame.K_b]
                    self.command_dict['right'] = key[pygame.K_m]
                    self.command_dict['jump'] = key[pygame.K_SPACE]
                    self.command_dict['attack1'] = key[pygame.K_o]
                    self.command_dict['attack2'] = key[pygame.K_p]
            time.sleep(0.01)  # Pequeno delay para evitar uso excessivo de CPU