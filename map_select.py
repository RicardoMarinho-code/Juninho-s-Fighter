import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from ui_components import (
    TITLE_FONT, HUD_FONT, WHITE, GRAY, YELLOW
)

def select_map(screen):
    # Lista de mapas disponíveis (adicione mais se quiser)
    maps = [
        {"name": "Aeroporto", "img": "assets/imagens/background/aeroporto.jpeg"},
        {"name": "Universidade Católica", "img": "assets/imagens/background/catolica.jpeg"},
        {"name": "Catedral", "img": "assets/imagens/background/catedral.jpeg"},
        {"name": "Congresso PDS", "img": "assets/imagens/background/congressoPDS.jpeg"},
        {"name": "Museu", "img": "assets/imagens/background/museu.jpeg"}
       
    
    ]
    num_maps = len(maps)
    current = 0

    title_font = TITLE_FONT
    small_font = HUD_FONT

    select_btn_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 120, 200, 60)
    select_btn_hover = False

    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill(GRAY)
        # Título
        title = title_font.render("Select Stage", True, WHITE)
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 60)))

        # Mostra imagem do mapa selecionado
        try:
            bg_img = pygame.image.load(maps[current]["img"]).convert()
            bg_img = pygame.transform.scale(bg_img, (500, 280))
            img_rect = bg_img.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(bg_img, img_rect)
        except:
            # Se não encontrar a imagem, mostra um retângulo cinza
            pygame.draw.rect(screen, (80,80,80), (SCREEN_WIDTH//2-250, SCREEN_HEIGHT//2-140, 500, 280))

        # Nome do mapa
        map_name = small_font.render(maps[current]["name"], True, YELLOW)
        screen.blit(map_name, map_name.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 170)))

        # Botão de seleção
        mouse = pygame.mouse.get_pos()
        select_btn_hover = select_btn_rect.collidepoint(mouse)
        btn_color = (0, 150, 255) if select_btn_hover else (0, 100, 200)
        pygame.draw.rect(screen, btn_color, select_btn_rect, border_radius=14)
        btn_text = title_font.render("START", True, WHITE)
        btn_rect = btn_text.get_rect(center=select_btn_rect.center)
        screen.blit(btn_text, btn_rect)

        # Instruções
        instr = small_font.render("←/→ para trocar de mapa", True, WHITE)
        screen.blit(instr, (SCREEN_WIDTH//2 - instr.get_width()//2, SCREEN_HEIGHT - 60))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                import sys
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current = (current - 1) % num_maps
                elif event.key == pygame.K_RIGHT:
                    current = (current + 1) % num_maps
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if select_btn_hover:
                    running = False

        clock.tick(60)

    return maps[current]["img"]