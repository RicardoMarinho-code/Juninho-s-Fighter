import pygame

"""
A classe de lutador é sobre um conteúdo do sétimo semestre, 
a programação orientada a objeto.

A programação orientada a objeto serve para criar classes e objetos,
que são instâncias de uma classe.
"""
class Fighter:
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound): #
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0 #0:idle #1:run #2:jump #3:attack1 #4: attack2 #5:hit #6:death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time =pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180)) #tamanho do retângulo. 80 de largura e 180 de altura
        self.vel_y = 0
        self.running = False
        self.jump = False #se não está pulando, False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.attack_sound = sound
        self.hit = False
        self.health = 100
        self.alive = True
        
    def load_images(self, sprite_sheet, animation_steps):
        #extrai as imagens do spritesheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img = pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale))
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list
    
    def move(self, screen_width, screen_height, surface, target, round_over):
        SPEED = 5
        GRAVITY =  2
        dx = 0 #direita ou esquerda
        dy = 0 #cima ou baixo
        self.running = False
        self.attack_type = 0

        key = pygame.key.get_pressed()  # corrigido aqui
        
        #pode fazer outras acoes se nao estiver atacando
        if self.attacking == False and self.alive == True and round_over == False:
            #checa os controles do player 1
            if self.player == 1:
                if key[pygame.K_a]:
                    dx = -SPEED #faz o lutador ir para a esquerda
                    self.running = True 
                if key[pygame.K_d]:
                    dx = SPEED #faz o lutador ir para a direita
                    self.running = True
                # pula
                if key[pygame.K_w] and self.jump == False: #quando pula uma vez, a opção de pulo fica desabilitada
                    self.vel_y = -30  #faz o lutador ir para cima
                    self.jump = True
                #ataque
                if key[pygame.K_r] or key[pygame.K_t]: 
                    self.attack(target)
                    #determina qual tipo de ataque foi usado
                    if key[pygame.K_r]:
                        self.attack_type = 1
                    if key[pygame.K_t]:
                        self.attack_type = 2
                        
            #checa os controles do player 2
            if self.player == 2:
                if key[pygame.K_b]:
                    dx = -SPEED #faz o lutador ir para a esquerda
                    self.running = True 
                if key[pygame.K_m]:
                    dx = SPEED #faz o lutador ir para a direita
                    self.running = True
                # pula
                if key[pygame.K_SPACE] and self.jump == False: #quando pula uma vez, a opção de pulo fica desabilitada
                    self.vel_y = -30  #faz o lutador ir para cima
                    self.jump = True
                #ataque
                if key[pygame.K_o] or key[pygame.K_p]: 
                    self.attack(target)
                    #determina qual tipo de ataque foi usado
                    if key[pygame.K_o]:
                        self.attack_type = 1
                    if key[pygame.K_p]:
                        self.attack_type = 2

        #coloca a gravidade
        self.vel_y += GRAVITY

        """
        Se colocar apenas o "self.vel_y += GRAVITY", que puxa o objeto para baixo,
        o objeto vai continuar indo para baixo mesmo que o jogador não esteja pressionando.
        Por isso, temps que conseguir um jeito de saber se o objeto está no chão ou não.
        """

        dy += self.vel_y #

        #confirma presenca do player na tela
        if self.rect.left + dx < 0:
            dx = 0 - self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 40:
            self.vel_y = 0
            self.jump = False #ativa o pulo quando o lutador toca o chão
            dy = screen_height - 40 - self.rect.bottom

        #certifica que os players olhem um para o outro
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True
            
        #aplica o cooldowm do ataque
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        #atualza a posição do jogador
        self.rect.x += dx
        self.rect.y += dy 
        
    #organiza as mudancas de animacao
    def update(self):
        #analisa qual acao o boneco esta fazendo
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6)#6: morto
        elif self.hit == True:
            self.update_action(5)#5: hit
        elif self.attacking == True:
           if self.attack_type == 1:
                self.update_action(3)#3: attack 1
           elif self.attack_type == 2:
               self.update_action(4)#4: attack 2
        elif self.jump == True:
            self.update_action(2)#2: pulando
        elif self.running == True:
            self.update_action(1)#1: correndo
        else:
            self.update_action(0)#0: parado
        
        
        animation_cooldown = 50 #dita a velocidade da animacao
        #atualiza as imagens
        self.image = self.animation_list[self.action][self.frame_index]
        #analisa se passou tempo suficiente desde o ultimo update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        #analisa se a animacao terminou
        if self.frame_index >= len(self.animation_list[self.action]):
            #checa se o player esta morto, entao termina a animacao
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                #checa se o ataque foi executado
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attack_cooldown = 20
                #checa se o boneco tomou dano
                if self.action == 5:
                    self.hit = False
                    #se o player estiver no meio de um ataque, entao para o ataque
                    self.attacking = False
                    self.attack_cooldown = 20

    def attack(self, target):
        if self.attack_cooldown == 0:
            #executa o ataque
            self.attacking = True
            self.attack_sound.play()
            attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
            if attacking_rect.colliderect(target.rect):
                target.health -= 10
                target.hit = True
        
    def update_action(self, new_action):
        #analisa se a nova acao difere da anterior
        if new_action != self.action:
            self.action = new_action
            #atualiza a configuracao da animacao
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):    #desenha o personagem
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
