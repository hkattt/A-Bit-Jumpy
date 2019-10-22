# Platformer Sprites

import pygame
from Platformer_Settings import *
vector = pygame.math.Vector2

class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        """Initializes hero"""
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.load_images()
        self.image = self.standing[0]
        self.rect = self.image.get_rect()
        self.position = vector(int(x * TILE_SIZE), int(y * TILE_SIZE))
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)
        self.shooting = False
        self.running = False
        self.frame_count = 0
        self.previous_U = 0
        self.right = False
        self.left = False
        self.arrow_timer = 0

    def do_jump(self):
        self.rect.x += 11
        collisions = pygame.sprite.spritecollide(self, self.game.environment, False)
        self.rect.x -= 11
        if collisions:
            self.velocity.y = -12

    def update(self):
        """Movement for the players hero"""
        self.animation()
        # This movement system was adapted from KidsCanCode Youtube channel.
        self.acceleration = vector(0, ACC)

        if self.arrow_timer > 0:
            self.arrow_timer += 1
        if self.arrow_timer == 100:
            self.arrow_timer = 0

        KEYS = pygame.key.get_pressed()
        if KEYS[pygame.K_LEFT]:
            self.acceleration.x = -ACC
            self.left, self.right = True, False
        if KEYS[pygame.K_RIGHT]:
            self.acceleration.x = ACC
            self.right, self.left = True, False

        for arrow in self.game.arrows:
            if arrow.rect.centerx  > WIDTH or arrow.rect.centerx < 0 or arrow.hit == True:
                self.game.arrows.remove(arrow)
                self.game.all_sprites.remove(arrow)
                
        if KEYS[pygame.K_s]:
            if len(self.game.arrows) < 5 and self.arrow_timer == 0:
                self.shooting = True
                self.arrow_timer = 1
                if self.right == True:
                    arrow = Arrow("r", self.game)
                else:
                    arrow = Arrow("l", self.game)

        # Friction
        self.acceleration += self.velocity * FRIC
        # Equations of motion
        self.velocity += self.acceleration
        if abs(self.velocity.x) < 0.2:
            self.velocity.x = 0
        self.position += self.velocity + 0.5 * self.acceleration 

        self.rect.midbottom = self.position

    def animation(self):
        current = pygame.time.get_ticks()
        # Shooting animation
        if self.shooting == True:
            if current - self.previous_U > 250:
                self.previous_U = current
                self.frame_count = (self.frame_count + 1) % len(self.bow_left)
                if self.frame_count == 12:
                    self.shooting = False
                if self.right:
                    self.image = self.bow_right[self.frame_count]
                else:
                    self.image = self.bow_left[self.frame_count]

        if self.velocity.x != 0:
            self.running = True
        else:
            self.running = False
        # Running animation
        if self.running:
            if current - self.previous_U > 250:
                self.previous_U = current
                self.frame_count = (self.frame_count + 1) % len(self.running_left) 
                if self.velocity.x > 0:
                    self.image = self.running_right[self.frame_count]
                else:
                    self.image = self.running_left[self.frame_count]
                
        # Idle animation (still)    
        if not self.running and not self.shooting:
            if current - self.previous_U > 300:
                self.previous_U = current
                self.frame_count = (self.frame_count + 1) % len(self.standing)
                self.image = self.standing[self.frame_count]

    def load_images(self):
        """Loads in images for sprite animation"""
        self.running_right = [pygame.image.load("hero_walking_right_1.png"), pygame.image.load("hero_walking_right_2.png"), pygame.image.load("hero_walking_right_3.png"), pygame.image.load("hero_walking_right_4.png"), pygame.image.load("hero_walking_right_5.png"), pygame.image.load("hero_walking_right_6.png"), pygame.image.load("hero_walking_right_7.png"), pygame.image.load("hero_walking_right_8.png"), pygame.image.load("hero_walking_right_9.png")]
        self.running_left = [pygame.image.load("hero_walking_left_1.png"), pygame.image.load("hero_walking_left_2.png"), pygame.image.load("hero_walking_left_3.png"), pygame.image.load("hero_walking_left_4.png"), pygame.image.load("hero_walking_left_5.png"), pygame.image.load("hero_walking_left_6.png"), pygame.image.load("hero_walking_left_7.png"), pygame.image.load("hero_walking_left_8.png"), pygame.image.load("hero_walking_left_9.png")]
        self.standing = [pygame.image.load("hero_standing_1.png"), pygame.image.load("hero_standing_2.png"), pygame.image.load("hero_standing_3.png"), pygame.image.load("hero_standing_4.png"), pygame.image.load("hero_standing_5.png"), pygame.image.load("hero_standing_6.png"), pygame.image.load("hero_standing_7.png")]
        self.bow_left = [pygame.image.load("hero_bow_left_1.png"), pygame.image.load("hero_bow_left_2.png"), pygame.image.load("hero_bow_left_3.png"), pygame.image.load("hero_bow_left_4.png"), pygame.image.load("hero_bow_left_5.png"), pygame.image.load("hero_bow_left_6.png"), pygame.image.load("hero_bow_left_7.png"), pygame.image.load("hero_bow_left_8.png"), pygame.image.load("hero_bow_left_9.png"), pygame.image.load("hero_bow_left_10.png"), pygame.image.load("hero_bow_left_11.png"), pygame.image.load("hero_bow_left_12.png"), pygame.image.load("hero_bow_left_13.png")]       
        self.bow_right = [pygame.image.load("hero_bow_right_1.png"), pygame.image.load("hero_bow_right_2.png"), pygame.image.load("hero_bow_right_3.png"), pygame.image.load("hero_bow_right_4.png"), pygame.image.load("hero_bow_right_5.png"), pygame.image.load("hero_bow_right_6.png"), pygame.image.load("hero_bow_right_7.png"), pygame.image.load("hero_bow_right_8.png"), pygame.image.load("hero_bow_right_9.png"), pygame.image.load("hero_bow_right_10.png"), pygame.image.load("hero_bow_right_11.png"), pygame.image.load("hero_bow_right_12.png"), pygame.image.load("hero_bow_right_13.png")]

class Environment(pygame.sprite.Sprite):
    def __init__(self, x, y, type, game):
        """Initiates environment block"""
        self.groups = game.all_sprites, game.environment
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.load_images()
        if type == "g":
            self.image = self.grass[0]
        elif type == "d":
            self.image = self.dirt
        self.rect = self.image.get_rect()
        self.rect.x = self.x * TILE_SIZE
        self.rect.y = self.y * TILE_SIZE

    def load_images(self):
        """Loads in images for the environment blocks"""
        self.grass = [pygame.image.load("grass_1.png"), pygame.image.load("grass_2.png"), pygame.image.load("grass_3.png")]
        self.dirt = pygame.image.load("dirt.png")
        #self.lava = pygame.image.load("lava.png")

class Arrow(pygame.sprite.Sprite):
    def __init__(self, direction, game):
        self.groups = game.all_sprites, game.arrows
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.load_images()
        if direction == "r":
            self.image = self.right_arrow
        if direction == "l":
            self.image = self.left_arrow
        self.position = self.game.hero.rect.center
        self.direction = direction
        self.velocity = vector(0, 0)
        self.acceleration = vector(0,0)
        self.rect = self.image.get_rect()
        self.start_timer = 0
        self.hit = False

    def update(self):
        if self.direction == "r":
            self.acceleration.x = 0.3
        if self.direction == "l":
            self.acceleration.x = -0.3
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5 * self.acceleration

        self.rect.center = self.position
        self.start_timer += 1

        collisions = pygame.sprite.spritecollide(self, self.game.environment, False)
        if collisions:
            if self.direction == "r":
                self.position.x = collisions[0].rect.left - 10
            if self.direction == "l":
                self.position.x = collisions[0].rect.right + 10
            self.velocity.x = 0
            self.hit = True

    def load_images(self):
        self.right_arrow = pygame.image.load("arrow_right.png")
        self.left_arrow = pygame.image.load("arrow_left.png")
