import pygame
from utils.constants import *

class Fighter:
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = IDLE
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
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

    def move(self, screen_width, screen_height, target, round_over):
        SPEED = 5
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        key = pygame.key.get_pressed()
        if not self.attacking and self.alive and not round_over:
            if self.player == 1:
                if key[pygame.K_a]: dx = -SPEED; self.running = True
                if key[pygame.K_d]: dx = SPEED; self.running = True
                if key[pygame.K_w] and not self.jump: self.vel_y = -30; self.jump = True
                if key[pygame.K_r] or key[pygame.K_t]:
                    self.attack(target)
                    self.attack_type = 1 if key[pygame.K_r] else 2
            elif self.player == 2:
                if key[pygame.K_b]: dx = -SPEED; self.running = True
                if key[pygame.K_m]: dx = SPEED; self.running = True
                if key[pygame.K_SPACE] and not self.jump: self.vel_y = -30; self.jump = True
                if key[pygame.K_o] or key[pygame.K_p]:
                    self.attack(target)
                    self.attack_type = 1 if key[pygame.K_o] else 2

        self.vel_y += GRAVITY
        dy += self.vel_y

        if self.rect.left + dx < 0: dx = 0 - self.rect.left
        if self.rect.right + dx > screen_width: dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 40:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 40 - self.rect.bottom

        self.flip = target.rect.centerx < self.rect.centerx

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        self.rect.x += dx
        self.rect.y += dy

    def update(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(DEATH)
        elif self.hit:
            self.update_action(HIT)
        elif self.attacking:
            self.update_action(ATTACK1 if self.attack_type == 1 else ATTACK2)
        elif self.jump:
            self.update_action(JUMP)
        elif self.running:
            self.update_action(RUN)
        else:
            self.update_action(IDLE)

        animation_cooldown = 50
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

    def attack(self, target):
        if self.attack_cooldown == 0:
            self.attacking = True
            self.attack_sound.play()
            attacking_rect = pygame.Rect(
                self.rect.centerx - (2 * self.rect.width * self.flip),
                self.rect.y, 2 * self.rect.width, self.rect.height
            )
            if attacking_rect.colliderect(target.rect):
                target.health -= 10
                target.hit = True

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
