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
        self.position = vector(int(x * TILE_SIZE), int(y * TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.position
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)
        self.shooting = False
        self.running = False
        self.frame_count = 0
        self.previous_U = 0
        self.right = False
        self.left = False
        self.arrow_timer = 0
        self.keys = []
        self.dead = False

    def wall_collisions(self):
        """Checks if the hero collides with the walls"""
        if self.velocity.y > 0:
            collisions = pygame.sprite.spritecollide(self, self.game.environment, False, pygame.sprite.collide_mask)
            if collisions:
                lowest = collisions[0]
                for collision in collisions:
                    if collision.rect.bottom > lowest.rect.bottom:
                        lowest = collision
                if self.position.y + 10 < lowest.rect.center[1]:
                    self.position.y = lowest.rect.top + 10
                    self.velocity.y = 0

        if abs(self.velocity.x) > 0 and abs(self.velocity.y) == 0:
            collisions = pygame.sprite.spritecollide(self, self.game.environment, False)
            if collisions:
                highest = collisions[0]
                for collision in collisions:
                    if collision.rect.bottom < highest.rect.bottom:
                        highest = collision
                    if self.rect.top > highest.rect.top:
                        if self.velocity.x > 0:
                            self.position.x = highest.rect.left - self.rect.width / 2 
                        elif self.velocity.x < 0:
                            self.position.x = highest.rect.right + self.rect.width / 2 
                        self.velocity.x = 0

    def get_keys(self):
         # This movement system was adapted from KidsCanCode Youtube channel.
        self.acceleration = vector(0, ACC)

        if self.arrow_timer > 0:
            self.arrow_timer += 1
        if self.arrow_timer == 50:
            self.arrow_timer = 0

        KEYS = pygame.key.get_pressed()
        if KEYS[pygame.K_LEFT]:
            self.acceleration.x = -ACC
            self.left, self.right = True, False
        if KEYS[pygame.K_RIGHT]:
            self.acceleration.x = ACC
            self.right, self.left = True, False
        if KEYS[pygame.K_UP]:
            if self.game.ladder.climb():
                self.acceleration.y = -ACC
        if KEYS[pygame.K_DOWN]:
            if self.game.ladder.climb():
                self.acceleration.y = ACC

        for arrow in self.game.arrows:
            if arrow.rect.centerx  > self.game.map.width or arrow.rect.centerx < 0 or arrow.hit == True:
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

    def do_jump(self):
        """Performs hero jump"""
        self.rect.x += 11
        collisions = pygame.sprite.spritecollide(self, self.game.environment, False)
        self.rect.x -= 11
        if collisions:
            self.velocity.y = -14

    def update(self):
        """Movement for the players hero"""
        self.animation()
        self.get_keys()
        self.wall_collisions()
        self.game.key.grab_key()
        self.game.spike.spike_hit()

    def animation(self):
        current = pygame.time.get_ticks()
        # Shooting animation
        if self.shooting == True:
            if current - self.previous_U > 50:
                self.previous_U = current
                self.frame_count = (self.frame_count + 1) % len(self.bow_left)
                if self.frame_count == 12:
                    self.shooting = False
                if self.right:
                    self.image = self.bow_right[self.frame_count]
                else:
                    self.image = self.bow_left[self.frame_count]

        if abs(self.velocity.x) > 0:
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

        self.mask = pygame.mask.from_surface(self.image)

    def load_images(self):
        """Loads in images for hero sprite animation"""
        self.running_right = [pygame.image.load("hero_walking_right_1.png"), pygame.image.load("hero_walking_right_2.png"), pygame.image.load("hero_walking_right_3.png"), pygame.image.load("hero_walking_right_4.png"), pygame.image.load("hero_walking_right_5.png"), pygame.image.load("hero_walking_right_6.png"), pygame.image.load("hero_walking_right_7.png"), pygame.image.load("hero_walking_right_8.png"), pygame.image.load("hero_walking_right_9.png")]
        self.running_left = [pygame.image.load("hero_walking_left_1.png"), pygame.image.load("hero_walking_left_2.png"), pygame.image.load("hero_walking_left_3.png"), pygame.image.load("hero_walking_left_4.png"), pygame.image.load("hero_walking_left_5.png"), pygame.image.load("hero_walking_left_6.png"), pygame.image.load("hero_walking_left_7.png"), pygame.image.load("hero_walking_left_8.png"), pygame.image.load("hero_walking_left_9.png")]
        self.standing = [pygame.image.load("hero_standing_1.png"), pygame.image.load("hero_standing_2.png"), pygame.image.load("hero_standing_3.png"), pygame.image.load("hero_standing_4.png"), pygame.image.load("hero_standing_5.png"), pygame.image.load("hero_standing_6.png"), pygame.image.load("hero_standing_7.png")]
        self.bow_left = [pygame.image.load("hero_bow_left_1.png"), pygame.image.load("hero_bow_left_2.png"), pygame.image.load("hero_bow_left_3.png"), pygame.image.load("hero_bow_left_4.png"), pygame.image.load("hero_bow_left_5.png"), pygame.image.load("hero_bow_left_6.png"), pygame.image.load("hero_bow_left_7.png"), pygame.image.load("hero_bow_left_8.png"), pygame.image.load("hero_bow_left_9.png"), pygame.image.load("hero_bow_left_10.png"), pygame.image.load("hero_bow_left_11.png"), pygame.image.load("hero_bow_left_12.png"), pygame.image.load("hero_bow_left_13.png")]       
        self.bow_right = [pygame.image.load("hero_bow_right_1.png"), pygame.image.load("hero_bow_right_2.png"), pygame.image.load("hero_bow_right_3.png"), pygame.image.load("hero_bow_right_4.png"), pygame.image.load("hero_bow_right_5.png"), pygame.image.load("hero_bow_right_6.png"), pygame.image.load("hero_bow_right_7.png"), pygame.image.load("hero_bow_right_8.png"), pygame.image.load("hero_bow_right_9.png"), pygame.image.load("hero_bow_right_10.png"), pygame.image.load("hero_bow_right_11.png"), pygame.image.load("hero_bow_right_12.png"), pygame.image.load("hero_bow_right_13.png")]

class Orc(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        """Initiates Orc"""
        self.groups = game.all_sprites, game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.load_images()
        self.position = vector(int(x * TILE_SIZE), int(y * TILE_SIZE))
        self.velocity = vector(0, 0) 
        self.image = self.walking_left[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.position
        self.health = 100
        self.frame_count = 0
        self.previous_U = 0
        self.left = True
        self.right = False

    def wall_collisions(self):
        """Checks if Orc collided with a wall"""
        if self.velocity.y > 0:
            collisions = pygame.sprite.spritecollide(self, self.game.environment, False)
            if collisions:
                lowest = collisions[0]
                for collision in collisions:
                    if collision.rect.bottom > lowest.rect.bottom:
                        lowest = collision
                if self.position.y + 10 < lowest.rect.center[1]:
                    self.position.y = lowest.rect.top - self.rect.height + 15
                    self.velocity.y = 0

        if abs(self.velocity.x) > 0:
                collisions = pygame.sprite.spritecollide(self, self.game.environment, False)
                if collisions:
                    highest = collisions[0]
                    for collision in collisions:
                        if collision.rect.bottom < highest.rect.bottom:
                            highest = collision
                        if self.rect.top > highest.rect.top:
                            if self.velocity.x > 0:
                                self.position.x = highest.rect.left - self.rect.width
                                self.right = False
                                self.left = True
                            elif self.velocity.x < 0:
                                self.position.x = highest.rect.right
                                self.left = False
                                self.right = True
                            self.velocity.x = 0

    def update(self):
        self.animation()
        self.move()
        self.wall_collisions()
        self.attack()
        if self.health == 0:
            self.game.enemies.remove(self)
            self.game.all_sprites.remove(self)

    def move(self):
        """Moves orc character"""
        self.acceleration = vector(0, ACC)
        #if abs(self.game.hero.position.x - self.position.x) < 350 and abs(self.game.hero.position.y - self.position.y) < 100:
        #    if self.game.hero.position.x > self.position.x:
                #self.acceleration.x = ACC
            #else:
            #    self.acceleration.x = -ACC
        
        # Friction
        self.acceleration += self.velocity * FRIC
        # Equations of motion
        self.velocity += self.acceleration
        if abs(self.velocity.x) < 0.2:
            self.velocity.x = 0
        self.position += self.velocity + 0.5 * self.acceleration
        self.rect.x, self.rect.y = self.position

    def attack(self):
        collisions = pygame.sprite.spritecollide(self.game.hero, self.game.enemies, False)
        if collisions:
            self.game.hero.dead = True

    def animation(self):
        current = pygame.time.get_ticks()
        if current - self.previous_U > 350:
                self.previous_U = current
                self.frame_count = (self.frame_count + 1) % len(self.walking_left) 
                if self.velocity.x > 0:
                    self.image = self.walking_right[self.frame_count]
                else:
                    self.image = self.walking_left[self.frame_count]

    def load_images(self):
        """Loads in images for Orc sprite animation"""
        self.walking_left = [pygame.image.load("orc_walking_left_1.png"), pygame.image.load("orc_walking_left_2.png"), pygame.image.load("orc_walking_left_3.png"), pygame.image.load("orc_walking_left_4.png"), pygame.image.load("orc_walking_left_5.png"), pygame.image.load("orc_walking_left_6.png"), pygame.image.load("orc_walking_left_7.png"), pygame.image.load("orc_walking_left_8.png"), pygame.image.load("orc_walking_left_9.png")]
        self.walking_right = [pygame.image.load("orc_walking_right_1.png"), pygame.image.load("orc_walking_right_2.png"), pygame.image.load("orc_walking_right_3.png"), pygame.image.load("orc_walking_right_4.png"), pygame.image.load("orc_walking_right_5.png"), pygame.image.load("orc_walking_right_6.png"), pygame.image.load("orc_walking_right_7.png"), pygame.image.load("orc_walking_right_8.png"), pygame.image.load("orc_walking_right_9.png"),]

class Spawner(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        """Initiates mob spawner"""
        self.groups = game.all_sprites, game.spawners
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.load_images()
        self.position = vector(int(x * TILE_SIZE), int(y * TILE_SIZE))
        self.image = self.tunnel[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.position
        self.previous_U = 0
        self.spawning = False

    def update(self):
        self.animation()

    def create_enemy(self):
        self.spawning = True
        return Orc(self.rect.x / TILE_SIZE, self.rect.y / TILE_SIZE, self.game)

    def animation(self):
        if self.spawning:
            current = pygame.time.get_ticks()
            self.image = self.tunnel[1]
            if current - self.previous_U > 8000:
                self.previous_U = current
                self.spawning = False
        else:
            self.image = self.tunnel[0]

    def load_images(self):
        """Loads in images for spawner animation"""
        self.tunnel = [pygame.image.load("tunnel_closed.png"), pygame.image.load("tunnel_open.png")]

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
        elif type == "gr":
            self.image = self.grass[1]
        elif type == "gl":
            self.image = self.grass[2]
        elif type == "hg":
            self.image = self.grass[3]
        elif type == "d":
            self.image = self.dirt
        elif type == "l":
            self.image = self.lava[0]
        elif type == "w":
            self.image = self.water
        elif type == "la":
            self.image = self.ladder
        self.type = type
        self.rect = self.image.get_rect()
        self.rect.x = self.x * TILE_SIZE
        self.rect.y = self.y * TILE_SIZE
        self.previous_U = 0
        self.frame_count = 0

    def load_images(self):
        """Loads in images for the environment blocks"""
        self.grass = [pygame.image.load("grass_1.png"), pygame.image.load("grass_2.png"), pygame.image.load("grass_3.png"), pygame.image.load("half.png")]
        self.dirt = pygame.image.load("dirt.png")
        self.lava = [pygame.image.load("lava_1.png"), pygame.image.load("lava_2.png"), pygame.image.load("lava_3.png")]
        self.water = pygame.image.load("water.png")

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
        self.hit_enemy()
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

    def hit_enemy(self):
        collisions = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if collisions:
            collisions[0].health = 0
            self.velocity.x = 0
            self.hit = True

    def load_images(self):
        self.right_arrow = pygame.image.load("arrow_right.png")
        self.left_arrow = pygame.image.load("arrow_left.png")

class Ladder(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        self.groups = game.all_sprites, game.ladders
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.load_images()
        self.image = self.ladder
        self.rect = self.image.get_rect()
        self.rect.x = self.x * TILE_SIZE
        self.rect.y = self.y * TILE_SIZE

    def climb(self):
        collisions = pygame.sprite.spritecollide(self.game.hero, self.game.ladders, False)
        if collisions:
            #self.game.hero.x, self.game.hero.y = self.rect.x, self.rect.y
            # self.game.hero.ladder = True
            return True
        return False

    def load_images(self):
        """Loads in images for the ladder blocks"""
        self.ladder = pygame.image.load("ladder_1.png")

class Spikes(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        """Initiates Spikes"""
        self.groups = game.all_sprites, game.spikes
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.load_images()
        self.position = vector(int(x * TILE_SIZE), int(y * TILE_SIZE))
        self.image = self.spikes
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.position
        self.mask = pygame.mask.from_surface(self.image)

    def spike_hit(self):
        collisions = pygame.sprite.spritecollide(self.game.hero, self.game.spikes, False, pygame.sprite.collide_mask)
        if collisions:
            self.game.hero.dead = True

    def load_images(self):
        """Loads in image for the spikes"""
        self.spikes = pygame.image.load("spikes.png")

class Key(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        """Initiates Key"""
        self.groups = game.all_sprites, game.keys
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.load_images()
        self.image = self.key
        self.position = vector(int(x * TILE_SIZE), int(y * TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.position
        self.mask = pygame.mask.from_surface(self.image)

    def load_images(self):
        """Loads in images for the key"""
        self.key = pygame.image.load("key_1.png")

    def grab_key(self):
        """Checks if the hero can pick up the key"""
        collisions = pygame.sprite.spritecollide(self.game.hero, self.game.keys, False, pygame.sprite.collide_mask)
        if collisions:
            self.game.hero.keys.append(collisions[0])
            self.game.keys.remove(collisions[0])
            self.game.all_sprites.remove(collisions[0])

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        """Initiates door"""
        self.groups = game.all_sprites, game.doors
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.load_images()
        self.position = vector(int(x * TILE_SIZE), int(y * TILE_SIZE))
        self.image = self.door[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.position
        self.open = False
    
    def update(self):
        self.animation()

    def animation(self):
        if len(self.game.hero.keys) > 0:
            collisions = pygame.sprite.spritecollide(self.game.hero, self.game.doors, False)
            if collisions:
                self.image = self.door[1]
            else:
                self.image = self.door[0]

    def load_images(self):
        """Loads in images for the door animation"""
        self.door = [pygame.image.load("door_closed.png"), pygame.image.load("door_open.png")]