# ui.py - Funções para desenhar texto, barra de vida e fundo
import pygame

# Função para desenhar texto na tela
def draw_text(text, font, color, x, y, surface):
    # Renderiza o texto e o desenha na tela
    img = font.render(text, True, color)
    surface.blit(img, (x, y))

# Função para desenhar a barra de vida do jogador
def draw_health_bar(health, x, y, surface):
    # Fundo preto com borda dourada
    pygame.draw.rect(surface, (255,215,0), (x-4, y-4, 404, 34), border_radius=12)
    pygame.draw.rect(surface, (30,30,30), (x, y, 396, 26), border_radius=10)
    # Barra de vida (gradiente vermelho-amarelo)
    ratio = max(0, health / 100)
    bar_width = int(396 * ratio)
    if bar_width > 0:
        for i in range(bar_width):
            color = (
                255,
                int(215 - 215 * (i/bar_width)),
                0
            )
            pygame.draw.line(surface, color, (x+i, y), (x+i, y+26), 1)

# Função para desenhar o fundo do jogo
def draw_background(background, surface, width, height):
    # Redimensiona e desenha o fundo na tela
    scaled_background = pygame.transform.scale(background, (width, height))
    surface.blit(scaled_background, (0, 0))
