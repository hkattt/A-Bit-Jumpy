# Platformer Sprites

# Imports required modules
import pygame
import random
# Imports settings file
from Platformer_Settings import *
from Platformer_Display import *
vector = pygame.math.Vector2

# Main game classes (for the platformer gameplay)

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
        self.armour = 0
        self.max_armour = 3
        self.dead = False
        self.coins = self.game.hero_coins
        self.max_coins = 999
        if self.game.difficulty == "normal":
            self.difficulty_multiplier = 1
        elif self.game.difficulty == "impossible":
            self.difficulty_multiplier = 0.5
        else:
            self.difficulty_multiplier = 100
    
    def update(self):
        """Updates the hero object"""
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
        # This movement system was adapted from KidsCanCode Youtube channel.
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
        collisions = pygame.sprite.spritecollide(self, self.game.environment, False)
        if collisions: # Checks if the player can jump (is on a platform)
            # Finds the lowest (closest to the bottom of the screen) block the player collided with
            lowest = collisions[0]
            for collision in collisions:
                if collision.rect.top > lowest.rect.top:
                    lowest = collision
            # Can only jump if the player is standing on the block (can not jump inside the block)
            if self.rect.bottom == lowest.rect.top + 10:
                if self.game.jump_pad.can_jump(): # Is on a jump pad
                    self.velocity.y = -10.2
                else:
                    self.velocity.y = -7

    def died(self):
        """Checks if the player died"""
        if self.hearts < 1:
            self.dead = True
        if self.position.x > self.game.map.width or self.position.y > self.game.map.height:
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
        self.cooldown = 0

    def wall_collisions(self):
        """Checks if Orc collided with a wall"""
        # Falling
        if self.velocity.y > 0:
            collisions = pygame.sprite.spritecollide(self, self.game.environment, False, pygame.sprite.collide_mask)
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
                            elif self.velocity.x < 0: # If the player is moving left
                                self.position.x = highest.rect.right
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
        #print(self.attack_cooldown, "die")
        if self.health <= 0:
            self.game.enemies.remove(self)
            self.game.orcs.remove(self)
            self.game.all_sprites.remove(self)
            if self.spawner != None:
                self.spawner.orcs.remove(self)

    def move(self):
        """Moves orc sprite"""
        self.acceleration = vector(0, ACC) # Applies gravity
        # Moves towards the player (hero) is they are on the same platform level and is within the x range (512 pixels)
        if abs(self.game.hero.position.x - self.position.x) < 512 and self.game.hero.rect.centery > self.rect.y and self.game.hero.rect.centery < self.rect.y + self.rect.height:
            # Moves to the right
            if self.game.hero.rect.centerx > self.position.x: 
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
        # Is not following the player
        else:
            # Finds the direction the orc should move
            if self.right:
                self.velocity.x = 1 
            else:
                self.velocity.x = -1
            # Applies gravity and horizontal velocity
            self.velocity += self.acceleration
            self.position += self.velocity
            
        self.rect.x, self.rect.y = self.position
        # Checks if the orc will fall off a platform
        if self.turn():
            self.rect.x -= self.velocity.x
            self.rect.y -= self.velocity.y

    def turn(self):
        """Checks if orc is going to walk off a platform"""
        collisions = pygame.sprite.spritecollide(self, self.game.environment, False, pygame.sprite.collide_mask)
        # If the orc is not collding with anything he must be falling
        if collisions:
            return False
        # Moving right
        if self.velocity.x > 0:
            self.right, self.left = False, True
        # Moving left
        else:
            self.right, self.left = True, False
        return True

    def can_attack(self):
        """Checks if the attack cool is over"""
        if self.cooldown > 0:
            self.cooldown += 1
        if self.cooldown  > 30:
            self.cooldown = 0
        if self.cooldown == 0:
            return True
        return False

    def attack(self):
        """Attacks the player"""
        # Attacks if the two sprite collide
        collisions = pygame.sprite.spritecollide(self.game.hero, self.game.orcs, False, pygame.sprite.collide_mask)
        if collisions:
            if collisions[0] == self:
                collisions[0].cooldown = 1
                # Deals damage
                if self.game.difficulty == "normal":
                    if self.game.hero.armour > 0:
                        self.game.hero.armour -= 1
                    else:
                        self.game.hero.hearts -= 1
                    
                elif self.game.difficulty == "impossible":
                    if self.game.hero.armour > 0:
                        self.game.hero.armour -= 3
                    else:
                        self.game.hero.hearts -= 3

    def animation(self):
        """Animates the orc sprite"""
        #print(self.attack_cooldown, "ani")
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
            self.mask = pygame.mask.from_surface(self.image)

    def load_images(self):
        """Loads in images for Orc sprite animation"""
        self.walking_left = [pygame.image.load("orc_walking_left_1.png"), pygame.image.load("orc_walking_left_2.png"), pygame.image.load("orc_walking_left_3.png"), pygame.image.load("orc_walking_left_4.png"), pygame.image.load("orc_walking_left_5.png"), pygame.image.load("orc_walking_left_6.png"), pygame.image.load("orc_walking_left_7.png"), pygame.image.load("orc_walking_left_8.png"), pygame.image.load("orc_walking_left_9.png")]
        self.walking_right = [pygame.image.load("orc_walking_right_1.png"), pygame.image.load("orc_walking_right_2.png"), pygame.image.load("orc_walking_right_3.png"), pygame.image.load("orc_walking_right_4.png"), pygame.image.load("orc_walking_right_5.png"), pygame.image.load("orc_walking_right_6.png"), pygame.image.load("orc_walking_right_7.png"), pygame.image.load("orc_walking_right_8.png"), pygame.image.load("orc_walking_right_9.png")]
        self.dead = pygame.image.load("orc_dead_1.png")

class Fly(pygame.sprite.Sprite):
    """Fly enemy object"""
    def __init__(self, x, y, game):
        """Initiates fly"""
        self.groups = game.all_sprites, game.flies, game.enemies # Fly groups
        # Initiates sprite class
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.load_images()
        self.position = vector(int(x * TILE_SIZE), int(y * TILE_SIZE))
        self.velocity = vector(random.choice([1, 1.5]), random.choice([1, 1.5]))
        self.acceleration = 0.2
        self.image = self.fly_left[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.position
        self.health = 200
        self.frame_count = 0
        self.previous_U = 0
        self.left = True
        self.right = False
        self.cooldown = 0

    def update(self):
        """Updates the fly sprite"""
        self.animation()
        self.move()
        if self.can_attack():
            self.attack()
        self.died()

    def can_attack(self):
        """Checks if the attack cool is over"""
        #print(self.rect.x, self.cooldown)
        if self.cooldown > 0:
            self.cooldown += 1
        if self.cooldown > 30:
            self.cooldown = 0
        if self.cooldown == 0:
            return True
        return False

    def attack(self):
        """Attacks the player"""
        # Attacks if the two sprite collide
        collisions = pygame.sprite.spritecollide(self.game.hero, self.game.flies, False, pygame.sprite.collide_mask)
        if collisions:
            if collisions[0] == self:
                collisions[0].cooldown = 1
                # Deals damage
                if self.game.difficulty == "normal" or self.game.difficulty == "impossible":
                    if self.game.hero.armour > 0:
                        self.game.hero.armour -= 3
                        if self.game.hero.armour < 3:
                            self.game.hero.armour = 0
                    else:
                        self.game.hero.hearts -= 3

    def died(self):
        """Checks if the fly died"""
        if self.health <= 0:
            self.game.enemies.remove(self)
            self.game.flies.remove(self)
            self.game.all_sprites.remove(self)

    def move(self):
        """Moves the fly sprite"""
        # Moves towards the hero (player) if they are within a certain range
        if abs(self.game.hero.rect.midtop[0] - self.position.x) < 512 and abs(self.game.hero.rect.midtop[1] - self.position.y) < 256:
            self.velocity = vector(random.choice([1, 1.5]), random.choice([1, 1.5]))
            # Moves to the right
            if self.game.hero.rect.midtop[0] > self.position.x:
                self.position.x += self.velocity.x
                self.right, self.left = True, False
            # Moves to the left
            else:
                self.position.x -= self.velocity.x
                self.right, self.left = False, True
            # Moves down
            if self.game.hero.rect.midtop[1] > self.position.y:
                self.position.y += self.velocity.y
            # Moves up
            else:
                self.position.y -= self.velocity.y

        else:
            self.velocity.y += self.acceleration
            self.position += self.velocity
            if abs(self.velocity.y) > 2:
                self.acceleration *= -1
            if self.velocity.x > 0:
                self.right, self.left = True, False
            else:
                self.right, self.left = False, True
            if self.position.x > self.game.map.width:
                self.velocity.x *= -1
            elif self.position.x < 0:
                self.velocity.x *= -1

        self.rect.x, self.rect.y = self.position

    def animation(self):
        """Animates the fly sprite"""
        current = pygame.time.get_ticks()
        if current - self.previous_U > 150: # Determines animation speed
            self.previous_U = current
            self.frame_count = (self.frame_count + 1) % len(self.fly_left) # Calculates the current frame
            # Moving right 
            if self.right:
                self.image = self.fly_right[self.frame_count]
            # Moving left
            else:
                self.image = self.fly_left[self.frame_count]

    def load_images(self):
        """Loads in images for fly animation"""
        self.fly_right = [pygame.image.load("fly_right_1.png"), pygame.image.load("fly_right_2.png")]
        self.fly_left = [pygame.image.load("fly_left_1.png"), pygame.image.load("fly_left_2.png")]
        self.fly_dead = [pygame.image.load("fly_right_dead.png"), pygame.image.load("fly_left_dead.png")]

class Spawner(pygame.sprite.Sprite):
    """ Orc spawner object"""
    def __init__(self, x, y, game):
        """Initiates orc spawner"""
        self.groups = game.all_sprites, game.spawners # Spawner group
        # Initiates the sprite class
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
        """Updates the spawner sprite"""
        self.animation()

    def create_enemy(self):
        """Spawns an orc enemy"""
        # Normal or god mode selected
        if self.game.difficulty == "normal" or self.game.difficulty == "god":
            # Only two orcs can be alive at any one time
            if len(self.orcs) < 2: 
                self.spawning = True
                return Orc(self.rect.x / TILE_SIZE, self.rect.y / TILE_SIZE, self.game, self)
        # Impossible difficulty
        elif self.game.difficulty == "impossible":
            # More orcs can be alive at once when playing on the impossible difficulty
            if len(self.orcs) < 4:
                self.spawning = True
                return Orc(self.rect.x / TILE_SIZE, self.rect.y / TILE_SIZE, self.game, self)

    def animation(self):
        """Animates the orc sprite"""
        # If an orc is being spawned
        if self.spawning:
            current = pygame.time.get_ticks()
            self.image = self.tunnel[1]
            if current - self.previous_U > 10000: # Door stays open for a short time after an orc is spawned
                self.previous_U = current
                self.spawning = False
        # Not spawning an orc
        else:
            self.image = self.tunnel[0]

    def load_images(self):
        """Loads in images for spawner animation"""
        self.tunnel = [pygame.image.load("tunnel_closed.png"), pygame.image.load("tunnel_open.png")]

class Environment(pygame.sprite.Sprite):
    """Environmental blocks (terrian)"""
    def __init__(self, x, y, type, game):
        """Initiates environment block"""
        self.groups = game.all_sprites, game.environment # Environment block groups
        # Initiates sprite class
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
    """Arrow object"""
    def __init__(self, direction, game):
        # Initiates arrow
        self.groups = game.all_sprites, game.arrows # Arrow groups
        # Initiates sprite class
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
        """Updates arrow sprite"""
        self.hit_enemy()
        self.hit_wall()
        self.move()   
        self.remove()

    def move(self):
        """Moves the arrow sprite"""
        # Moving right
        if self.direction == "r":
            self.acceleration.x = 0.3
        # Moving left
        if self.direction == "l":
            self.acceleration.x = -0.3
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5 * self.acceleration

        self.rect.center = self.position
        # Starts the arrow cooldown
        self.start_timer += 1

    def hit_enemy(self):
        """Checks if the arrow struck an enemy"""
        collisions = pygame.sprite.spritecollide(self, self.game.enemies, False)
        # If the arrow hit an enemy
        if collisions:
            # Deals damage
            collisions[0].health -= self.damage * self.game.hero.difficulty_multiplier
            self.velocity.x = 0
            self.hit = True
            self.remove()
    
    def hit_wall(self):
        """Checks if the arrow hit a wall"""
        collisions = pygame.sprite.spritecollide(self, self.game.environment, False)
        # Hit a wall
        if collisions:
            # Moving right
            if self.direction == "r":
                self.position.x = collisions[0].rect.left - 10
            # Moving left
            if self.direction == "l":
                self.position.x = collisions[0].rect.right + 10
            self.velocity.x = 0
            self.hit = True

    def remove(self):
        """Removes arrow from sprite groups"""
        # If the arrow hit a object or is off the map
        if self.rect.centerx  > self.game.map.width or self.rect.centerx < 0 or self.hit == True:
            self.game.arrows.remove(self)
            self.game.all_sprites.remove(self)

    def load_images(self):
        """Loads in arrow images"""
        self.right_arrow = pygame.image.load("arrow_right.png")
        self.left_arrow = pygame.image.load("arrow_left.png")

class Jump_Pad(pygame.sprite.Sprite):
    """Jump pad object"""
    def __init__(self, x, y, game):
        """Initiates jump pad"""
        self.groups = game.all_sprites, game.jump_pads # Jump pad groups
        # Initiates sprite class
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
        """Updates the jump pad sprite"""
        self.animation()
    
    def animation(self):
        """Animates the jump pad"""
        # If the jump pad is being used 
        if self.jumping:
            current = pygame.time.get_ticks()
            self.image = self.jump_pad[1]
            if current - self.previous_U > 5500: # Jump pad is extended for a short time after it is used
                self.previous_U = current
                self.jumping = False
        # Not being used
        else:
            self.image = self.jump_pad[0]

    def can_jump(self):
        """Checks if the hero (player) can use the jump pad"""
        collisions = pygame.sprite.spritecollide(self.game.hero, self.game.jump_pads, False, pygame.sprite.collide_mask)
        # Is standing on jump pad
        if collisions: 
            collisions[0].jumping = True
            return True
        return False

    def load_images(self):
        """Loads in images for the jump pad animation"""
        self.jump_pad = [pygame.image.load("jump_pad_1.png"), pygame.image.load("jump_pad_2.png")]

class Spikes(pygame.sprite.Sprite):
    """Spike object"""
    def __init__(self, x, y, game):
        """Initiates Spike"""
        self.groups = game.all_sprites, game.spikes # Spike groups
        # Initiates sprite class
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.load_images()
        self.position = vector(int(x * TILE_SIZE), int(y * TILE_SIZE))
        self.image = self.spikes
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.position
        # Creates an image mask for collisions
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        """Updates the spike sprite"""
        self.spike_hit()

    def spike_hit(self):
        """Checks if the player landed on a spike"""
        collisions = pygame.sprite.spritecollide(self.game.hero, self.game.spikes, False, pygame.sprite.collide_mask)
        # Landed on a spike
        if collisions:
            # Deals damage
            # Armour does not block it
            if self.game.difficulty == "normal" or self.game.difficulty == "impossible":
                self.game.hero.hearts -= 3

    def load_images(self):
        """Loads in image for the spikes"""
        self.spikes = pygame.image.load("spikes.png")

class Key(pygame.sprite.Sprite):
    """Key object"""
    def __init__(self, x, y, game):
        """Initiates Key"""
        self.groups = game.all_sprites, game.keys # Key groups
        # Initiates the sprite class
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.load_images()
        self.image = self.key
        # Makes the image smaller
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.position = vector(int(x * TILE_SIZE + 17), int(y * TILE_SIZE + 17))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.position
        # Creates an image mask for collisions
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        """Updates the key sprite"""
        self.grab_key()

    def grab_key(self):
        """Checks if the hero can pick up the key"""
        collisions = pygame.sprite.spritecollide(self.game.hero, self.game.keys, False, pygame.sprite.collide_mask)
        # Can pick up the key
        if collisions:
            # Gives hero object the key
            self.game.hero.keys.append(collisions[0])
            self.game.keys.remove(collisions[0])
            self.game.all_sprites.remove(collisions[0])

    def load_images(self):
        """Loads in image for the key"""
        self.key = pygame.image.load("key_1.png")

class Door(pygame.sprite.Sprite):
    """Door object"""
    def __init__(self, x, y, game):
        """Initiates door"""
        self.groups = game.all_sprites, game.doors # Door groups
        # Initiates sprite class
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
        """Updates the door sprite"""
        self.animation()
        # Checks if the player beat the level
        if self.complete_level():
            self.game.level += 1
            self.game.playing = False

    def animation(self):
        """Animates door sprite"""
        # If the player has collected all the keys
        if len(self.game.keys) == 0:
            collisions = pygame.sprite.spritecollide(self.game.hero, self.game.doors, False)
            # If the player is standing on the door it will open
            if collisions:
                self.image = self.door[1]
            # Player is not on the door
            else:
                self.image = self.door[0]

    def complete_level(self):
        """Checks if the player has passed the level"""
        # Has collected all the keys
        if len(self.game.keys) == 0:
            collisions = pygame.sprite.spritecollide(self.game.hero, self.game.doors, False)
            # Is standing on the door
            if collisions:
                return True
        return False

    def load_images(self):
        """Loads in images for the door animation"""
        self.door = [pygame.image.load("door_closed.png"), pygame.image.load("door_open.png")]

class Coin(pygame.sprite.Sprite):
    """Coin object"""
    def __init__(self, x, y, game):
        """Initiates coin"""
        self.groups = game.all_sprites, game.coins # Coin groups
        # Initiates sprite class
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
        """Updates coin sprite"""
        self.pick_up()
        self.animation()

    def animation(self):
        """Animates coin sprite"""
        current = pygame.time.get_ticks()
        if current - self.previous_U > 100: # Animation speed
            self.previous_U = current
            self.frame_count = (self.frame_count + 1) % len(self.coin) # Calculates the current frame 
            self.image = self.coin[self.frame_count]
            self.image = pygame.transform.scale(self.image, (30, 30)) # Makes the image smaller
            self.mask = pygame.mask.from_surface(self.image) # Creates an image mask for collisions

    def pick_up(self):
        """Checks if the hero can pick up the coin"""
        collisions = pygame.sprite.spritecollide(self.game.hero, self.game.coins, False, pygame.sprite.collide_mask)
        # Player is standing on the coin
        if collisions:
            # Hero gets the coin
            if self.game.difficulty == "impossible":
                coin = random.randint(1, 2)
                if coin == 1:
                    self.game.hero.coins += 1
            else:
                self.game.hero.coins += 1 * self.game.hero.difficulty_multiplier
            if self.game.hero.coins > self.game.hero.max_coins:
                self.game.hero.coins = self.game.hero.max_coins
            self.game.all_sprites.remove(collisions[0])
            self.game.coins.remove(collisions[0])

    def load_images(self):
        """Loads in images for coin animation"""
        self.coin = [pygame.image.load("coin_1.png"), pygame.image.load("coin_2.png"), pygame.image.load("coin_3.png"), pygame.image.load("coin_4.png"), pygame.image.load("coin_5.png"), pygame.image.load("coin_6.png")]

# Town classes (For when the hero is in the town)

class Town_Hero(pygame.sprite.Sprite):
    """Town hero"""
    def __init__(self, x, y, town):
        """Initiates town hero"""
        self.groups = town.all_sprites # Hero groups
        # Initiates the sprite class
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.town = town
        self.load_images()
        self.image = self.walking_right[0]
        self.position = vector(int(x * TILE_SIZE), int(y * TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.position
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)
        self.frame_count = 0
        self.previous_U = 0
        self.right = True
        self.left = False
        self.up = False
        self.down = False
        self.mask = pygame.mask.from_surface(self.image) # Creates an image mask for collisions

    def update(self):
        """Updates hero sprite"""
        #self.animation()
        self.get_keys()
        self.move()
        self.animation()

    def get_keys(self):
        """Gets key events from the user"""
        self.acceleration = vector(0, 0)
        KEYS = pygame.key.get_pressed()
        # Moving left
        if KEYS[pygame.K_LEFT] or KEYS[pygame.K_a]: 
            self.acceleration.x = -ACC
            self.right, self.left, self.up, self.down = False, True, False, False
        # Moving right
        elif KEYS[pygame.K_RIGHT] or KEYS[pygame.K_d]:
            self.acceleration.x = ACC
            self.right, self.left, self.up, self.down = True, False, False, False
        # Moving up
        elif KEYS[pygame.K_UP] or KEYS[pygame.K_w]:
            self.acceleration.y = -ACC
            self.right, self.left, self.up, self.down = False, False, True, False
        # Moving down
        elif KEYS[pygame.K_DOWN] or KEYS[pygame.K_s]:
            self.acceleration.y = ACC
            self.right, self.left, self.up, self.down = False, False, False, True
        elif KEYS[pygame.K_LSHIFT] or KEYS[pygame.K_RSHIFT]:
            if self.town.shop.can_shop():
                self.town.shop.shop()
 
    def move(self):
        """Moves the sprite"""
        # Friction
        self.acceleration += self.velocity * FRIC
        # Equations of motion
        self.velocity += self.acceleration
        if abs(self.velocity.x) < 0.2:
            self.velocity.x = 0
        if abs(self.velocity.y) < 0.2:
            self.velocity.y = 0
        # Used to determine if the player stopped moving
        if abs(self.velocity.x) < 0.2:
            self.right, self.left = False, False
        if abs(self.velocity.y) < 0.2:
            self.up, self.down = False, False
        self.position += self.velocity + 0.5 * self.acceleration
        self.rect.x = self.position.x
        self.collision("x")
        self.rect.y = self.position.y
        self.collision("y")
    
    def animation(self):
        """Animates the hero sprite"""
        current = pygame.time.get_ticks()
        # Checks if the player is running
        if current - self.previous_U > 150: # Animation speed
            self.previous_U = current
            self.frame_count = (self.frame_count + 1) % len(self.walking_left) 
            # Moving right
            if self.right:
                self.image = self.walking_right[self.frame_count]
            # Moving left
            elif self.left:
                self.image = self.walking_left[self.frame_count]
            # Moving down
            elif self.down:
                self.image = self.walking_down[self.frame_count]
            # Moving up
            elif self.up:
                self.image = self.walking_up[self.frame_count]
            
        # Creates an image mask for collisions
        self.mask = pygame.mask.from_surface(self.image)

    def collision(self, direction):
        """Checks for collisions (if the player went off the dirt track)"""
        if direction == "x":
            collisions = pygame.sprite.spritecollide(self.town.hero, self.town.town_blocks, False)
            if collisions:
                if self.velocity.x > 0:
                    self.position.x = collisions[0].rect.left - self.rect.width
                if self.velocity.x < 0:
                    self.position.x = collisions[0].rect.right
                self.velocity.x = 0
                self.rect.x = self.position.x
        elif direction == "y":
            collisions = pygame.sprite.spritecollide(self.town.hero, self.town.town_blocks, False)
            if collisions:
                if self.velocity.y > 0:
                    self.position.y = collisions[0].rect.top - self.rect.height
                elif self.velocity.y < 0:
                    self.position.y = collisions[0].rect.bottom
                self.velocity.y = 0
                self.rect.y = self.position.y

    def load_images(self):
        """Loads in images for hero sprite animation"""
        self.walking_right = [pygame.image.load("hero_walking_right_1.png"), pygame.image.load("hero_walking_right_2.png"), pygame.image.load("hero_walking_right_3.png"), pygame.image.load("hero_walking_right_4.png"), pygame.image.load("hero_walking_right_5.png"), pygame.image.load("hero_walking_right_6.png"), pygame.image.load("hero_walking_right_7.png"), pygame.image.load("hero_walking_right_8.png"), pygame.image.load("hero_walking_right_9.png")]
        self.walking_left = [pygame.image.load("hero_walking_left_1.png"), pygame.image.load("hero_walking_left_2.png"), pygame.image.load("hero_walking_left_3.png"), pygame.image.load("hero_walking_left_4.png"), pygame.image.load("hero_walking_left_5.png"), pygame.image.load("hero_walking_left_6.png"), pygame.image.load("hero_walking_left_7.png"), pygame.image.load("hero_walking_left_8.png"), pygame.image.load("hero_walking_left_9.png")]
        self.walking_up = [pygame.image.load("hero_walking_up_1.png"), pygame.image.load("hero_walking_up_2.png"), pygame.image.load("hero_walking_up_3.png"), pygame.image.load("hero_walking_up_4.png"), pygame.image.load("hero_walking_up_5.png"), pygame.image.load("hero_walking_up_6.png"), pygame.image.load("hero_walking_up_7.png"), pygame.image.load("hero_walking_up_8.png"), pygame.image.load("hero_walking_up_9.png")]
        self.walking_down = [pygame.image.load("hero_walking_down_1.png"), pygame.image.load("hero_walking_down_2.png"), pygame.image.load("hero_walking_down_3.png"), pygame.image.load("hero_walking_down_4.png"), pygame.image.load("hero_walking_down_5.png"), pygame.image.load("hero_walking_down_6.png"), pygame.image.load("hero_walking_down_7.png"), pygame.image.load("hero_walking_down_8.png"), pygame.image.load("hero_walking_down_9.png")]

class Town_Terrain(pygame.sprite.Sprite):
    """Town environment"""
    def __init__(self, x, y, type, town):
        """Initiates town terrain"""
        self.groups = town.all_sprites, town.town_blocks # Town terrain groups
        # Initiates sprite class
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.type = type
        self.load_images()
        # Different image depending on the block type
        if type == "g":
            self.image = self.grass
        elif type[0] == "w":
            if type[1:] == "tl":
                self.image = self.water[0]
            elif type[1:] == "tm":
                self.image = self.water[1]
            elif type[1:] == "tr":
                self.image = self.water[2]
            elif type[1:] == "ml":
                self.image = self.water[3]
            elif type[1:] == "mm":
                self.image = self.water[4]
            elif type[1:] == "mr":
                self.image = self.water[5]
            elif type[1:] == "bl":
                self.image = self.water[6]
            elif type[1:] == "bm":
                self.image = self.water[7]
            elif type[1:] == "br":
                self.image = self.water[8]
        self.rect = self.image.get_rect()
        self.rect.x = self.x * TILE_SIZE
        self.rect.y = self.y * TILE_SIZE

    def load_images(self):
        """Loads in images for town environment"""
        self.grass = pygame.image.load("town_grass.png")
        self.water = [pygame.image.load("water_tl.png"), pygame.image.load("water_tm.png"), pygame.image.load("water_tr.png"), pygame.image.load("water_ml.png"), pygame.image.load("water_mm.png"), pygame.image.load("water_mr.png"), pygame.image.load("water_bl.png"), pygame.image.load("water_bm.png"), pygame.image.load("water_br.png")]

class Decorations(pygame.sprite.Sprite):
    """Decorations in the town"""
    def __init__(self, x, y, type, town):
        """Initiates decorations"""
        self.groups = town.all_sprites, town.decorations # Town decorations groups
        # Initiates sprite class
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.type = type
        self.load_images()
        # Different image depending on the block type
        if type[1] == "1":
            self.image = self.bush[0]
        elif type[1] == "2":
            self.image = self.bush[1]
        elif type[1] == "3":
            self.image = self.bush[2]
        self.rect = self.image.get_rect()
        self.rect.x = self.x * TILE_SIZE
        self.rect.y = self.y * TILE_SIZE

    def load_images(self):
        """Loads in images for decoration objects"""
        self.bush = [pygame.image.load("bush_1.png"), pygame.image.load("bush_2.png"), pygame.image.load("bush_3.png")]

class Town_Path(pygame.sprite.Sprite):
    """Town path"""
    def __init__(self, x, y, type, town):
        """Initiates town path"""
        self.groups = town.all_sprites, town.path_blocks # Path groups
        # Initiates sprite class
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.type = type
        self.load_images()
        # Different image depending on the block type
        if type[1:] == "tl":
            self.image = self.dirt[0]
        elif type[1:] == "tm":
            self.image = self.dirt[1]
        elif type[1:] == "tr":
            self.image = self.dirt[2]
        elif type[1:] == "ml":
            self.image = self.dirt[3]
        elif type[1:] == "mm":
            self.image = self.dirt[4]
        elif type[1:] == "mr":
            self.image = self.dirt[5]
        elif type[1:] == "bl":
            self.image = self.dirt[6]
        elif type[1:] == "bm":
            self.image = self.dirt[7]
        elif type[1:] == "br":
            self.image = self.dirt[8]
        self.rect = self.image.get_rect()
        self.rect.x = self.x * TILE_SIZE
        self.rect.y = self.y * TILE_SIZE

    def load_images(self):
        self.dirt = [pygame.image.load("dirt_tl.png"), pygame.image.load("dirt_tm.png"), pygame.image.load("dirt_tr.png"), pygame.image.load("dirt_ml.png"), pygame.image.load("dirt_mm.png"), pygame.image.load("dirt_mr.png"), pygame.image.load("dirt_bl.png"), pygame.image.load("dirt_bm.png"), pygame.image.load("dirt_br.png")]

class Town_Door(pygame.sprite.Sprite):
    """Door to move into the platformer level"""
    def __init__(self, x, y, town):
        """Initiates the town door"""
        self.groups = town.all_sprites, town.town_doors
        # Initiates the sprite class
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.town = town
        self.load_images()
        self.image = self.closed
        self.position = vector(int(x * TILE_SIZE), int(y * TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.position
        self.mask = pygame.mask.from_surface(self.image) # Creates an image mask for collisions

    def update(self):
        """Updates the town door"""
        self.animation()
        if self.go_to_game():
            self.town.playing = False

    def go_to_game(self):
        """Checks if the player wants to go back into the game"""
        collisions = pygame.sprite.spritecollide(self.town.hero, self.town.town_doors, False, pygame.sprite.collide_mask)
        if collisions:
            return True
        return False

    def animation(self):
        """Animates the town door"""
        collisions = pygame.sprite.spritecollide(self.town.hero, self.town.town_doors, False)
        # Open if the hero is standing on it
        if collisions:
            self.image = self.open
        # Closed if the hero is not standing on it
        else:
            self.image = self.closed

    def load_images(self):
        """Loads in iamges for door animation"""
        self.open = pygame.image.load("town_door_open.png")
        self.closed = pygame.image.load("town_door_closed.png")

class Town_Shop(pygame.sprite.Sprite):
    """Shops in which player can buy upgrades"""
    def __init__(self, x, y, type, town):
        self.groups = town.all_sprites, town.building_tiles
        # Initiates the sprite class
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.town = town
        self.load_images()
        if type[1] == "f":
            self.image = self.building[0]
        elif type[1] == "m":
            self.image = self.building[1]
        elif type[1] == "b":
            self.image = self.building[2]
        elif type[1] == "t":
            self.image = self.building[3]
        elif type[1] == "d":
            self.image = self.building[4]
        elif type[1] == "D":
            self.image = self.door[0]
        self.type = type
        self.position = vector(int(x * TILE_SIZE), int(y * TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.position
        self.previous_U = 0
        self.mask = pygame.mask.from_surface(self.image) # Creates an image mask for collisions

    def update(self):
        self.animation()

    def animation(self):
        collisions = pygame.sprite.spritecollide(self.town.hero, self.town.building_tiles, False)
        # Open if the hero is standing on it
        if self.type == "rD":
            if collisions:
                if collisions[0] == self:
                    self.image = self.door[1]
                    # Closed if the hero is not standing on it
            else:
                self.image = self.door[0]

    def can_shop(self):
        collisions = pygame.sprite.spritecollide(self.town.hero, self.town.building_tiles, False, pygame.sprite.collide_mask)
        # Open if the hero is standing on it
        if self.type == "rD":
            if collisions:
                return True
        return False

    def shop(self):
        shopping = True
        screen_outline = pygame.draw.rect(self.town.game.screen, BLACK, ((WIDTH / 2) - WIDTH / 3, HEIGHT / 5, WIDTH / 1.5, HEIGHT / 1.5), 0)        
        screen = pygame.draw.rect(self.town.game.screen, WHITE, ((WIDTH / 2) + 2 - WIDTH / 3, (HEIGHT / 5) + 2, (WIDTH / 1.5) - 4, (HEIGHT / 1.5) - 4), 0)
        self.shop_heading = Button(GREY[0], WIDTH / 2, HEIGHT / 3.5, 250, 50, "Shop", 40, self.town.game)
        self.armour = Button(GREY[0], WIDTH / 2, HEIGHT / 2, 200, 50, "Armour: " + str(int(5 / self.town.game.hero.difficulty_multiplier)) + " gold", 25, self.town.game)
        self.health = Button(GREY[0], WIDTH / 2, HEIGHT / 1.5, 200, 50, "Medicine: " + str(int(10 / self.town.game.hero.difficulty_multiplier)) + " gold" , 25, self.town.game)
        while shopping:
            position = pygame.mouse.get_pos()
            self.shop_heading.draw(self.town.game.screen)
            self.armour.draw(self.town.game.screen)
            self.health.draw(self.town.game.screen)
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    shopping = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        shopping = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.armour.mouse_over(position):
                        if self.town.game.hero.armour < self.town.game.hero.max_armour:
                            self.town.game.hero.armour += 1
                    if self.health.mouse_over(position):
                        if self.town.game.hero.hearts < 3:
                            self.town.game.hero.hearts = 3

                if event.type == pygame.MOUSEMOTION:
                        if self.armour.mouse_over(position):
                            self.armour.colour = GREY[1]
                        else:
                            self.armour.colour = GREY[0]
                        if self.health.mouse_over(position):
                            self.health.colour = GREY[1]
                        else:
                            self.health.colour = GREY[0]
                
            

        self.town.hero.rect.y += 64

    def load_images(self):
        """loads in images for building tiles"""
        self.building = [pygame.image.load("roof_f.png"), pygame.image.load("roof_m.png"), pygame.image.load("roof_b.png"), pygame.image.load("roof_tile.png"), pygame.image.load("door_frame.png")]
        self.door = [pygame.image.load("building_door_closed.png"), pygame.image.load("building_door_open.png")]