# pause_menu.py
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT

# Definição de cores RGB
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
BLUE = (0, 150, 255)
LIGHT_BLUE = (100, 200, 255)
DARK_BLUE = (0, 100, 200)

# Inicializa fontes para botões e título
pygame.font.init()
button_font = pygame.font.SysFont('Arial', 48)
title_font = pygame.font.SysFont('Arial', 60)

# Classe para criar botões interativos
class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, press_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.press_color = press_color
        self.hovered = False
        self.pressed = False

    # Desenha o botão na tela
    def draw(self, surface):
        color = self.press_color if self.pressed else (self.hover_color if self.hovered else self.color)
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        text_surf = button_font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    # Verifica se o mouse está sobre o botão
    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)

# Função que exibe o menu de pausa
def show_pause_menu(screen, stop_event=None, input_thread1=None, input_thread2=None):
    clock = pygame.time.Clock()
    # Cria os botões de continuar e sair
    continue_btn = Button("Continuar", SCREEN_WIDTH//2 - 100, 250, 200, 60, BLUE, LIGHT_BLUE, DARK_BLUE)
    quit_btn = Button("Sair", SCREEN_WIDTH//2 - 100, 350, 200, 60, BLUE, LIGHT_BLUE, DARK_BLUE)

    while True:
        screen.fill(GRAY)
        mouse_pos = pygame.mouse.get_pos()

        # Título do menu de pausa
        title_surf = title_font.render("PAUSADO", True, WHITE)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title_surf, title_rect)

        # Desenha os botões e verifica hover
        for btn in [continue_btn, quit_btn]:
            btn.check_hover(mouse_pos)
            btn.draw(screen)

        # Trata eventos do mouse e do sistema
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for btn in [continue_btn, quit_btn]:
                    if btn.hovered:
                        btn.pressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                for btn in [continue_btn, quit_btn]:
                    if btn.pressed and btn.hovered:
                        if btn == continue_btn:
                            return  # Sai do menu de pausa e continua o jogo
                        elif btn == quit_btn:
                            # Finaliza as threads de input e encerra o jogo
                            if stop_event: stop_event.set()
                            if input_thread1: input_thread1.join()
                            if input_thread2: input_thread2.join()
                            pygame.quit()
                            exit()
                for btn in [continue_btn, quit_btn]:
                    btn.pressed = False

        pygame.display.flip()
        clock.tick(60)
