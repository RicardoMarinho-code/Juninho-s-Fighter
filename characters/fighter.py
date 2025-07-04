# fighter.py - Classe que representa os personagens jogáveis (lutadores)
import pygame
from utils.constants import *  # Importa constantes como IDLE, ATTACK1, etc.

BLOCK = 7  # Nova ação (bloqueio)

class Fighter:
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound):
        # Inicializa atributos do personagem
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip

        # Carrega as animações do personagem
        self.animation_list = self.load_images(sprite_sheet, animation_steps)

        # Estado inicial do personagem
        self.action = IDLE
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()

        # Posição e física
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.attack_sound = sound
        self.hit = False
        self.health = 100
        self.alive = True

        # Novos atributos para combo e bloqueio
        self.combo_counter = 0
        self.timer_combo = 0 # Tempo para fazer combo novamente
        self.timer_ragdoll = 0 # Tempo para se levantar denovo
        self.last_hit_time = 0
        self.combo_timeout = 1000
        self.blocking = False  # Inicializa o atributo

        # Exemplo de dicionário de comandos para cada player
        self.cmd_p1 = {'left': False, 'right': False, 'jump': False, 'block': False, 'attack1': False, 'attack2': False}
        self.cmd_p2 = {'left': False, 'right': False, 'jump': False, 'block': False, 'attack1': False, 'attack2': False}

    # Carrega as imagens das animações a partir do sprite sheet
    def load_images(self, sprite_sheet, animation_steps):
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img = pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale))
                temp_img_list.append(temp_img)
            animation_list.append(temp_img_list)
        return animation_list

    # Atualiza a posição e estado do personagem conforme comandos e física
    def move(self, screen_width, screen_height, target, round_over, commands):
        SPEED = 7
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False

        # Só permite movimento se não estiver atacando, estiver vivo, não estiver levando hit e o round não acabou
        if not self.attacking and self.alive and not round_over:
            if self.hit:
                # Durante hit, só aplica knockback leve (ver abaixo)
                return
            if commands['left']: dx = -SPEED; self.running = True
            if commands['right']: dx = SPEED; self.running = True
            if commands['jump'] and not self.jump: self.vel_y = -30; self.jump = True
            self.blocking = commands.get('block', False)
            if commands['attack1'] or commands['attack2']:
                self.attack(target)
                self.attack_type = 1 if commands['attack1'] else 2

        self.vel_y += GRAVITY
        dy += self.vel_y

        # Limita o personagem dentro da tela
        if self.rect.left + dx < 0: dx = 0 - self.rect.left
        if self.rect.right + dx > screen_width: dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 40:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 40 - self.rect.bottom

        # Vira o personagem para o oponente
        self.flip = target.rect.centerx < self.rect.centerx

        # Reduz cooldown do ataque
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Atualiza posição
        self.rect.x += dx
        self.rect.y += dy

    # Atualiza o estado de animação do personagem
    def update(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(DEATH)
        elif self.hit:
            self.attacking = False  # Impede atacar durante hit
            self.update_action(HIT)
        elif self.attacking:
            self.update_action(ATTACK1 if self.attack_type == 1 else ATTACK2)
        elif self.blocking:
            self.update_action(BLOCK)
        elif self.jump:
            self.update_action(JUMP)
        elif self.running:
            self.update_action(RUN)
        else:
            self.update_action(IDLE)

        animation_cooldown = 27
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0 if self.alive else len(self.animation_list[self.action]) - 1
            if self.action in (ATTACK1, ATTACK2):
                self.attacking = False
                self.attack_cooldown = ATTACK_COOLDOWN
            if self.action == HIT:
                self.hit = False
                self.attacking = False
                self.attack_cooldown = ATTACK_COOLDOWN

    # Realiza o ataque no oponente
    def attack(self, target):
        if self.attack_cooldown == 0:
            self.attacking = True
            self.attack_sound.play()
            attacking_rect = pygame.Rect(
                self.rect.centerx - (2 * self.rect.width * self.flip),
                self.rect.y, 2 * self.rect.width, self.rect.height
            )
            current_time = pygame.time.get_ticks()
            # Lógica de combo: se atacar rápido, aumenta o contador
            if current_time - self.last_hit_time <= self.combo_timeout:
                self.combo_counter += 1
            else:
                self.combo_counter = 1
            self.last_hit_time = current_time

            # Se acertar o oponente
            if attacking_rect.colliderect(target.rect):
                if target.blocking and target.combo_counter < 2:
                    damage = 3
                else:
                    damage = 10
                target.health -= damage
                target.hit = True

                # Knockback leve em cada hit, exceto no 4º hit (ragdoll)
                if self.combo_counter == 4:
                    knockback = -170 if not target.flip else 170
                    target.rect.x += knockback
                    target.combo_counter = 0  # reseta combo após o lançamento
                else:
                    # Knockback leve
                    knockback = -15 if not target.flip else 15
                    target.rect.x += knockback

    # Atualiza a ação de animação
    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    # Desenha o personagem na tela
    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
