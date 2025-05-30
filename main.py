import pygame
import pygame.image
from pygame import mixer
from figher import Fighter

mixer.init()
pygame.init()

#cria janela
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Juninho's Fighter")

#define a framerat
clock = pygame.time.Clock()
fps = 60

#define as cores
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

#define variaveis do jogo
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]#scores dos players. [p1, p2]
round_over = False
ROUND_OVER_COOLDOWN = 2000
round_over_time = 0

#define algumas variaves dos bonecos
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE,WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

#carrega as musicas e sons
pygame.mixer.music.load("assets/audio/WhatsApp-Audio-2025-05-29-at-15.05.08.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.1)
magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
magic_fx.set_volume(0.25)

#carrega imagem de fundo
background = pygame.image.load("assets/imagens/Background/background1.jpeg").convert_alpha()

#carrega os sprites dos bonecos
warrior_sheet = pygame.image.load("assets/imagens/warrior/sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/imagens/wizard/sprites/wizard.png").convert_alpha()

#carrega a imagem da vitoria
victory_img = pygame.image.load("assets/imagens/icons/victory.png").convert_alpha()

#define o numero de passos para cada animacao
WARRIOR_ANIMATIONS_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATIONS_STEPS = [8, 8, 1, 8, 8, 3, 7]

#define a fonte
count_font = pygame.font.Font("assets/font/turok.ttf", 80)
score_font = pygame.font.Font("assets/font/turok.ttf", 80)

#funcao para desenhar o texto
def drawn_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#função para desenhar o fundo
def draw_background():
    scaled_background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT)) 
    screen.blit(scaled_background, (0, 0))

#funcao das barras de vida
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2,y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

#cria instâncias de jogador
player_1 = Fighter(1, 200, 380, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATIONS_STEPS, sword_fx) #posição x e y, para aparecer na tela
player_2 = Fighter(2, 700, 380, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATIONS_STEPS, magic_fx)

#loop para manter a janela aberta
run = True  
while run:
    
    #define a framerate
    clock.tick(fps)

    #desenha o fundo
    draw_background()
    
    #mostra os status do personagem
    draw_health_bar(player_1.health, 20, 20)
    draw_health_bar(player_2.health, 580, 20)
    drawn_text("P1: " + str(score[0]), score_font, RED, 20, 60)
    drawn_text("P2: " + str(score[1]), score_font, RED, 580, 60)
    
    if intro_count <= 0:
        #move os personagens
        player_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, player_2, round_over)
        player_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, player_1, round_over)
    else:
        #desenha na tela o timer
        drawn_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2,   SCREEN_HEIGHT / 3)
        #atualiza o contador
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()
    
    #atualiza as animacoses
    player_1.update()
    player_2.update()

    #desenha os lutadores
    player_1.draw(screen)
    player_2.draw(screen)

    #Checa se alguns dos players perdeu
    if round_over == False:
        if player_1.alive == False:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
            print(score)
        elif player_2.alive == False:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        #display victory image
        screen.blit(victory_img, (360, 150))
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 3
            player_1 = Fighter(1, 200, 380, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATIONS_STEPS, sword_fx)
            player_2 = Fighter(2, 700, 380, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATIONS_STEPS, magic_fx)
      
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 

    #atualiza a tela
    pygame.display.update()

pygame.quit()