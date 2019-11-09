# Platformer Sprites

# Imports required modules
import pygame
import random
# Imports settings file
from Platformer_Settings import *
vector = pygame.math.Vector2

class Hero(pygame.sprite.Sprite):
    """Hero (player) object"""
    def __init__(self, x, y, game):
        """Initializes hero"""
        self.groups = game.all_sprites # Hero groups
        # Initiates the sprite class
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
        self.hearts = 3
        self.dead = False
        self.coins = 0
    
    def update(self):
        """Upadtes the hero object"""
        self.animation()
        self.get_keys()
        self.move()
        self.wall_collisions()
        self.died()

    def wall_collisions(self):
        """Checks if the hero collides with the walls"""
        # Falling
        if self.velocity.y > 0: 
            collisions = pygame.sprite.spritecollide(self, self.game.environment, False, pygame.sprite.collide_mask)
            if collisions: # Checks if the player had a collision
                # Finds the lowest (closest to the bottom of the window) environmental block the player collided with
                lowest = collisions[0]
                for collision in collisions:
                    if collision.rect.bottom > lowest.rect.bottom:
                        lowest = collision
                if self.position.y + 10 < lowest.rect.center[1]: # If the player is below the ground (sprite image)
                    self.position.y = lowest.rect.top + 10
                    self.velocity.y = 0

        # Moving left or right and is not jumping or falling 
        if abs(self.velocity.x) > 0 and abs(self.velocity.y) == 0:
            collisions = pygame.sprite.spritecollide(self, self.game.environment, False)
            if collisions: # Checks if the player had a collision
                # Finds the highest (furthest from the bottom of the window) environmental block the player collided with
                highest = collisions[0]
                for collision in collisions:
                    if collision.rect.bottom < highest.rect.bottom:
                        highest = collision
                    if self.rect.top > highest.rect.top: # Below the highest environmental block
                        # Moving right 
                        if self.velocity.x > 0: 
                            self.position.x = highest.rect.left - self.rect.width / 2 
                        # Moving left
                        elif self.velocity.x < 0:
                            self.position.x = highest.rect.right + self.rect.width / 2 
                        self.velocity.x = 0

    def get_keys(self):
        """Gets the users key inputs (events)"""
         # This movement system was adapted from KidsCanCode Youtube channel.
        self.acceleration = vector(0, ACC) # Applies gravity
        # Arrow cooldown 
        if self.arrow_timer > 0:
            self.arrow_timer += 1
        if self.arrow_timer == 50:
            self.arrow_timer = 0

        KEYS = pygame.key.get_pressed()
        # Moving left
        if KEYS[pygame.K_LEFT] or KEYS[pygame.K_a]: 
            self.acceleration.x = -ACC
            self.left, self.right = True, False
        # Moving right
        if KEYS[pygame.K_RIGHT] or KEYS[pygame.K_d]:
            self.acceleration.x = ACC
            self.right, self.left = True, False
        # Jump
        if KEYS[pygame.K_UP] or KEYS[pygame.K_w]:
            self.do_jump()
        # Shoot       
        if KEYS[pygame.K_LSHIFT] or KEYS[pygame.K_RSHIFT]:
            if len(self.game.arrows) < 5 and self.arrow_timer == 0:
                self.shooting = True
                self.arrow_timer = 1
                if self.right == True:
                    arrow = Arrow("r", self.game)
                else:
                    arrow = Arrow("l", self.game)

    def move(self):
        """Moves the hero sprite"""
        # Friction
        self.acceleration.x += self.velocity.x * FRIC
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
        if collisions: # Checks if the player can jump (is on a platform)
            if self.game.jump_pad.can_jump(): # Is on a jump pad
                self.velocity.y = -10
            else:
                self.velocity.y = -7

    def died(self):
        """Checks if the player died"""
        if self.hearts < 1:
            self.dead = True

    def animation(self):
        """Animates the hero sprite"""
        current = pygame.time.get_ticks()
        # Shooting animation
        if self.shooting == True:
            if current - self.previous_U > 50: # Determines the speed of the animation
                self.previous_U = current
                self.frame_count = (self.frame_count + 1) % len(self.bow_left) # Calculates the correct frame
                if self.frame_count == 12: 
                    self.shooting = False
                # Looking right
                if self.right:
                    self.image = self.bow_right[self.frame_count]
                # Looking right
                else:
                    self.image = self.bow_left[self.frame_count]

        # Checks if the player is running
        if abs(self.velocity.x) > 0:
            self.running = True
        else:
            self.running = False

        # Running animation
        if self.running:
            if current - self.previous_U > 100: # Animation speed
                self.previous_U = current
                self.frame_count = (self.frame_count + 1) % len(self.running_left) 
                # Moving right
                if self.velocity.x > 0: 
                    self.image = self.running_right[self.frame_count]
                # Moving left
                else:
                    self.image = self.running_left[self.frame_count]

        # Creates an image mask for collisions
        self.mask = pygame.mask.from_surface(self.image)

    def load_images(self):
        """Loads in images for hero sprite animation"""
        self.running_right = [pygame.image.load("hero_walking_right_1.png"), pygame.image.load("hero_walking_right_2.png"), pygame.image.load("hero_walking_right_3.png"), pygame.image.load("hero_walking_right_4.png"), pygame.image.load("hero_walking_right_5.png"), pygame.image.load("hero_walking_right_6.png"), pygame.image.load("hero_walking_right_7.png"), pygame.image.load("hero_walking_right_8.png"), pygame.image.load("hero_walking_right_9.png")]
        self.running_left = [pygame.image.load("hero_walking_left_1.png"), pygame.image.load("hero_walking_left_2.png"), pygame.image.load("hero_walking_left_3.png"), pygame.image.load("hero_walking_left_4.png"), pygame.image.load("hero_walking_left_5.png"), pygame.image.load("hero_walking_left_6.png"), pygame.image.load("hero_walking_left_7.png"), pygame.image.load("hero_walking_left_8.png"), pygame.image.load("hero_walking_left_9.png")]
        self.standing = [pygame.image.load("hero_standing_1.png"), pygame.image.load("hero_standing_2.png"), pygame.image.load("hero_standing_3.png"), pygame.image.load("hero_standing_4.png"), pygame.image.load("hero_standing_5.png"), pygame.image.load("hero_standing_6.png"), pygame.image.load("hero_standing_7.png")]
        self.bow_left = [pygame.image.load("hero_bow_left_1.png"), pygame.image.load("hero_bow_left_2.png"), pygame.image.load("hero_bow_left_3.png"), pygame.image.load("hero_bow_left_4.png"), pygame.image.load("hero_bow_left_5.png"), pygame.image.load("hero_bow_left_6.png"), pygame.image.load("hero_bow_left_7.png"), pygame.image.load("hero_bow_left_8.png"), pygame.image.load("hero_bow_left_9.png"), pygame.image.load("hero_bow_left_10.png"), pygame.image.load("hero_bow_left_11.png"), pygame.image.load("hero_bow_left_12.png"), pygame.image.load("hero_bow_left_13.png")]       
        self.bow_right = [pygame.image.load("hero_bow_right_1.png"), pygame.image.load("hero_bow_right_2.png"), pygame.image.load("hero_bow_right_3.png"), pygame.image.load("hero_bow_right_4.png"), pygame.image.load("hero_bow_right_5.png"), pygame.image.load("hero_bow_right_6.png"), pygame.image.load("hero_bow_right_7.png"), pygame.image.load("hero_bow_right_8.png"), pygame.image.load("hero_bow_right_9.png"), pygame.image.load("hero_bow_right_10.png"), pygame.image.load("hero_bow_right_11.png"), pygame.image.load("hero_bow_right_12.png"), pygame.image.load("hero_bow_right_13.png")]

class Orc(pygame.sprite.Sprite):
    """Orc enemy object"""
    def __init__(self, x, y, game, spawner):
        """Initiates Orc"""
        self.groups = game.all_sprites, game.orcs, game.enemies # Orc groups
        # Initiates the sprite class
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
        self.spawner = spawner
        self.attack_cooldown = 0

    def wall_collisions(self):
        """Checks if Orc collided with a wall"""
        # Falling
        if self.velocity.y > 0:
            collisions = pygame.sprite.spritecollide(self, self.game.environment, False)
            if collisions: # Checks if the orc had a collision
                # Finds the lowest environment block the player collided with
                lowest = collisions[0]
                for collision in collisions:
                    if collision.rect.bottom > lowest.rect.bottom:
                        lowest = collision
                if self.position.y + 10 < lowest.rect.center[1]: # If the orc is below the ground
                    self.position.y = lowest.rect.top - self.rect.height + 15
                    self.velocity.y = 0

        # Moving left or right
        if abs(self.velocity.x) > 0:
                collisions = pygame.sprite.spritecollide(self, self.game.environment, False)
                if collisions: # Checks if the orc had a collision
                    # Finds the highest environment block the orc collided with
                    highest = collisions[0]
                    for collision in collisions:
                        if collision.rect.bottom < highest.rect.bottom:
                            highest = collision
                        # If the orc is below the highest environment block
                        if self.rect.top > highest.rect.top:
                            if self.velocity.x > 0: # If the player is moving right
                                self.position.x = highest.rect.left - self.rect.width
                                self.right = False
                                self.left = True
                            elif self.velocity.x < 0: # If the player is moving left
                                self.position.x = highest.rect.right
                                self.left = False
                                self.right = True
                            self.velocity.x = 0

    def update(self):
        """Updates the orc sprite"""
        self.animation()
        self.move()
        self.wall_collisions()
        if self.can_attack():
            self.attack()
        self.died()
    
    def died(self):
        """Checks if the orc died"""
        if self.health == 0:
            self.game.enemies.remove(self)
            self.game.orcs.remove(self)
            self.game.all_sprites.remove(self)
            if self.spawner != None:
                self.spawner.orcs.remove(self)

    def move(self):
        """Moves orc sprite"""
        self.acceleration = vector(0, ACC) # Applies gravity
        # Moves towards the player (hero) is they are on the screen display and are on the same platform
        if abs(self.game.hero.position.x - self.position.x) < 1024 and abs(self.game.hero.position.y - self.position.y) < 100:
            # Moves to the right
            if self.game.hero.position.x > self.position.x: 
                self.acceleration.x = ORC_ACC
            # Moves to the left
            else:
                self.acceleration.x = -ORC_ACC
        
        # Friction
        self.acceleration += self.velocity * ORC_FRIC
        # Equations of motion
        self.velocity += self.acceleration
        if abs(self.velocity.x) < 0.2:
            self.velocity.x = 0
        self.position += self.velocity + 0.5 * self.acceleration
        self.rect.x, self.rect.y = self.position

    def can_attack(self):
        """Checks if the attack cooldown is over"""
        if self.attack_cooldown > 0:
            self.attack_cooldown += 1
        if self.attack_cooldown > 30:
            self.attack_cooldown = 0
        if self.attack_cooldown == 0:
            return True
        return False

    def attack(self):
        """Attacks the player"""
        # Attacks if the two sprites collide
        collisions = pygame.sprite.spritecollide(self.game.hero, self.game.orcs, False, pygame.sprite.collide_mask)
        if collisions:
            self.attack_cooldown = 1
            self.game.hero.hearts -= 1

    def animation(self):
        """Animates the orc sprite"""
        current = pygame.time.get_ticks()
        if current - self.previous_U > 350: # Determines the animation speed
            self.previous_U = current
            self.frame_count = (self.frame_count + 1) % len(self.walking_left) # Calculates the current frame 
            # Walking right
            if self.velocity.x > 0:
                self.image = self.walking_right[self.frame_count]
            # Walking left
            else:
                self.image = self.walking_left[self.frame_count]

    def load_images(self):
        """Loads in images for Orc sprite animation"""
        self.walking_left = [pygame.image.load("orc_walking_left_1.png"), pygame.image.load("orc_walking_left_2.png"), pygame.image.load("orc_walking_left_3.png"), pygame.image.load("orc_walking_left_4.png"), pygame.image.load("orc_walking_left_5.png"), pygame.image.load("orc_walking_left_6.png"), pygame.image.load("orc_walking_left_7.png"), pygame.image.load("orc_walking_left_8.png"), pygame.image.load("orc_walking_left_9.png")]
        self.walking_right = [pygame.image.load("orc_walking_right_1.png"), pygame.image.load("orc_walking_right_2.png"), pygame.image.load("orc_walking_right_3.png"), pygame.image.load("orc_walking_right_4.png"), pygame.image.load("orc_walking_right_5.png"), pygame.image.load("orc_walking_right_6.png"), pygame.image.load("orc_walking_right_7.png"), pygame.image.load("orc_walking_right_8.png"), pygame.image.load("orc_walking_right_9.png")]

class Fly(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        """Initiates fly"""
        self.groups = game.all_sprites, game.flies, game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.load_images()
        self.position = vector(int(x * TILE_SIZE), int(y * TILE_SIZE))
        self.velocity = vector(random.choice([1, 1.5]), random.choice([1, 1.5]))
        self.image = self.fly_left[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.position
        self.health = 200
        self.frame_count = 0
        self.previous_U = 0
        self.left = True
        self.right = False

    def update(self):
        self.animation()
        self.move()
        self.died()

    def died(self):
        if self.health == 0:
            self.game.enemies.remove(self)
            self.game.flies.remove(self)
            self.game.all_sprites.remove(self)

    def move(self):
        #self.velocity.y += self.acceleration
        if abs(self.game.hero.rect.midtop[0] - self.position.x) < 512 and abs(self.game.hero.rect.midtop[1] - self.position.y) < 256:
            if self.game.hero.rect.midtop[0] > self.position.x:
                self.position.x += self.velocity.x
                self.right, self.left = True, False
            else:
                self.position.x -= self.velocity.x
                self.right, self.left = False, True
            if self.game.hero.rect.midtop[1] > self.position.y:
                self.position.y += self.velocity.y
            else:
                self.position.y -= self.velocity.y
        #self.velocity.y += self.acceleration
        #self.position.y += self.velocity.y
        self.rect.x, self.rect.y = self.position
        #if abs(self.velocity.y) > 1:
        #    self.acceleration *= -1

    def animation(self):
        current = pygame.time.get_ticks()
        if current - self.previous_U > 150:
            self.previous_U = current
            self.frame_count = (self.frame_count + 1) % len(self.fly_left) 
            if self.right:
                self.image = self.fly_right[self.frame_count]
            else:
                self.image = self.fly_left[self.frame_count]

    def load_images(self):
        self.fly_right = [pygame.image.load("fly_right_1.png"), pygame.image.load("fly_right_2.png")]
        self.fly_left = [pygame.image.load("fly_left_1.png"), pygame.image.load("fly_left_2.png")]
        self.fly_dead = [pygame.image.load("fly_right_dead.png"), pygame.image.load("fly_left_dead.png")]

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
        self.orcs = []

    def update(self):
        self.animation()

    def create_enemy(self):
        if len(self.orcs) < 3:
            self.spawning = True
            return Orc(self.rect.x / TILE_SIZE, self.rect.y / TILE_SIZE, self.game, self)

    def animation(self):
        if self.spawning:
            current = pygame.time.get_ticks()
            self.image = self.tunnel[1]
            if current - self.previous_U > 10000:
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
        self.damage = 100
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
            collisions[0].health -= self.damage
            self.velocity.x = 0
            self.hit = True
            self.remove()

    def remove(self):
        if self.rect.centerx  > self.game.map.width or self.rect.centerx < 0 or self.hit == True:
            self.game.arrows.remove(self)
            self.game.all_sprites.remove(self)

    def load_images(self):
        self.right_arrow = pygame.image.load("arrow_right.png")
        self.left_arrow = pygame.image.load("arrow_left.png")

class Jump_Pad(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        self.groups = game.all_sprites, game.jump_pads
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.load_images()
        self.image = self.jump_pad[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.x * TILE_SIZE
        self.rect.y = self.y * TILE_SIZE
        self.jumping = False
        self.previous_U = 0
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.animation()
    
    def animation(self):
        if self.jumping:
            current = pygame.time.get_ticks()
            self.image = self.jump_pad[1]
            if current - self.previous_U > 5500:
                self.previous_U = current
                self.jumping = False
        else:
            self.image = self.jump_pad[0]

    def can_jump(self):
        collisions = pygame.sprite.spritecollide(self.game.hero, self.game.jump_pads, False, pygame.sprite.collide_mask)
        if collisions:
            collisions[0].jumping = True
            return True
        return False

    def load_images(self):
        """Loads in images for the ladder blocks"""
        self.jump_pad = [pygame.image.load("jump_pad_1.png"), pygame.image.load("jump_pad_2.png")]

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

    def update(self):
        self.spike_hit()

    def spike_hit(self):
        collisions = pygame.sprite.spritecollide(self.game.hero, self.game.spikes, False, pygame.sprite.collide_mask)
        if collisions:
            self.game.hero.hearts -= 3

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
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.position = vector(int(x * TILE_SIZE + 17), int(y * TILE_SIZE + 17))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.position
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.grab_key()

    def grab_key(self):
        """Checks if the hero can pick up the key"""
        collisions = pygame.sprite.spritecollide(self.game.hero, self.game.keys, False, pygame.sprite.collide_mask)
        if collisions:
            self.game.hero.keys.append(collisions[0])
            self.game.keys.remove(collisions[0])
            self.game.all_sprites.remove(collisions[0])

    def load_images(self):
        """Loads in images for the key"""
        self.key = pygame.image.load("key_1.png")

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
        if self.complete_level():
            self.game.level += 1
            self.game.playing = False

    def animation(self):
        if len(self.game.keys) == 0:
            collisions = pygame.sprite.spritecollide(self.game.hero, self.game.doors, False)
            if collisions:
                self.image = self.door[1]
            else:
                self.image = self.door[0]

    def complete_level(self):
        if len(self.game.keys) == 0:
            collisions = pygame.sprite.spritecollide(self.game.hero, self.game.doors, False)
            if collisions:
                return True
        return False

    def load_images(self):
        """Loads in images for the door animation"""
        self.door = [pygame.image.load("door_closed.png"), pygame.image.load("door_open.png")]

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        """Initiates coin"""
        self.groups = game.all_sprites, game.coins
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.load_images()
        self.position = vector(int(x * TILE_SIZE + 17), int(y * TILE_SIZE + 17))
        self.image = self.coin[0]
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.position
        self.up = True
        self.down = False
        self.previous_U = 0
        self.frame_count = 0
    
    def update(self):
        self.pick_up()
        self.animation()

    def animation(self):
        current = pygame.time.get_ticks()
        if current - self.previous_U > 100:
            self.previous_U = current
            self.frame_count = (self.frame_count + 1) % len(self.coin) 
            self.image = self.coin[self.frame_count]
            self.image = pygame.transform.scale(self.image, (30, 30))
            self.mask = pygame.mask.from_surface(self.image)

    def pick_up(self):
        collisions = pygame.sprite.spritecollide(self.game.hero, self.game.coins, False, pygame.sprite.collide_mask)
        if collisions:
            self.game.hero.coins += 1
            self.game.all_sprites.remove(collisions[0])
            self.game.coins.remove(collisions[0])

    def load_images(self):
        """Loads in images for the coin"""
        self.coin = [pygame.image.load("coin_1.png"), pygame.image.load("coin_2.png"), pygame.image.load("coin_3.png"), pygame.image.load("coin_4.png"), pygame.image.load("coin_5.png"), pygame.image.load("coin_6.png")]