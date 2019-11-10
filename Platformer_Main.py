# Platformer main file

# Importing required modules
import pygame
import random
import time
# Imports other game files
from Platformer_Settings import *
from Platformer_Sprites import *
from Platformer_Camera import *
from Platformer_Display import *

#background = pygame.image.load("green_background.png")

class Game():
    """Game object"""
    def __init__(self):
        """Initialize game window and pygame"""
        pygame.init() 
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) # Game window
        pygame.display.set_caption("Platformer") # Game windows caption
        self.clock = pygame.time.Clock()
        self.running = True
        self.level = 1
        self.hero_coins = 0

    def load_map(self):
        """Loads in map (level)"""
        self.map = Map(self.level)
 
    def new(self):
        """Starts new game"""
        self.load_map()
        # Creates different sprite groups, used for collisions
        self.all_sprites = pygame.sprite.Group()
        self.spawners = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.orcs = pygame.sprite.Group()
        self.flies = pygame.sprite.Group()
        self.environment = pygame.sprite.Group()
        self.arrows = pygame.sprite.Group()
        self.jump_pads = pygame.sprite.Group()
        self.keys = pygame.sprite.Group()
        self.doors = pygame.sprite.Group()
        self.spikes = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.display_objects = pygame.sprite.Group()
        # Cycles through map array
        for row, tiles in enumerate(self.map.tile_map):
            for column, tile in enumerate(tiles):
                # Creates object based on the list items (string)
                if tile != ".":
                    if tile == "P":
                        self.hero_x, self.hero_y = column, row
                    elif tile == "D":
                        self.door = Door(column, row, self)
                    elif tile == "s":
                        self.spike = Spikes(column, row, self)
                    elif tile == "O":
                        self.orc = Orc(column, row, self, None)
                    elif tile == "F":
                        Fly(column, row, self)
                    elif tile == "c":
                        self.coin = Coin(column, row, self)
                    elif tile == "S":
                        self.spawner = Spawner(column, row, self)
                    elif tile == "K":
                        self.key = Key(column, row, self)
                    elif tile == "j":
                        self.jump_pad = Jump_Pad(column, row, self)
                    else:
                        self.environment_block = Environment(column, row, tile, self)
        self.camera = Camera(self.map.width, self.map.height)
        # Hero attribute display objects
        self.health_display = Health(0, 0, self)
        self.key_display = Key_Display(1, 0, self)
        self.coin_display = Coin_Count(2, 0, self)
        self.hero = Hero(self.hero_x, self.hero_y, self)
        self.enemy_timer = 0
        self.run()

    def run(self):
        """Main game loop"""
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.paint()

    def update(self):
        """Updates Window"""
        current = pygame.time.get_ticks()
        # Spawns an Orc enemy 
        if current - self.enemy_timer > ENEMY_SPAWN + random.choice([-1000, 0, 1000, 3000]):
            self.enemy_timer = current 
            for spawner in self.spawners:
                self.enemy = spawner.create_enemy()
                if self.enemy != None:
                    spawner.orcs.append(self.enemy)
        # Updates all the sprite objects and display objects
        self.all_sprites.update()
        self.display_objects.update()
        # Camera follows the player sprite
        self.camera.update(self.hero)

    def events(self):
        """Game loops events"""
        for event in pygame.event.get():
            # Checks if the user wants to quit the game
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
        # Checks if the player died
        if self.hero.dead == True:
            self.playing = False
            self.level = 1 # Resets the game level

    def paint(self):  
        """Draws onto the window"""
        self.screen.fill(SKY_BLUE) # Makes the display windows background blue

        # Moves every sprite object based on the camera position, then displays it onto the window
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.move_sprite(sprite))
        # Displays the players attributes onto the screen
        for sprite in self.display_objects:
            self.screen.blit(sprite.image, sprite)
        # Players coin count
        self.write(str(self.hero.coins), WHITE, 45, self.coin_display.position.x + self.coin_display.coin_space, self.coin_display.position.y + 32)
        pygame.display.update()

    def write(self, text, colour, size, x, y):
        """Draws text onto the screen"""
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, colour)
        text_rect = text_surface.get_rect()
        text_rect.center = x, y
        self.screen.blit(text_surface, text_rect)

    def start_screen(self):
        """Games start screen"""
        self.screen.fill(LIGHT_GREEN[0]) # Makes the windows background green
        self.write("Platformer", WHITE, 60, WIDTH / 2, HEIGHT / 5)
        self.write("Move and jumper with arrows or WASD, shoot with Shift", WHITE, 25, WIDTH / 2, HEIGHT / 2)
        self.write("Press any key to play!", WHITE, 25, WIDTH / 2, HEIGHT / 1.5)
        pygame.display.update()
        self.wait() # Waits for user input 
        
    def end_screen(self):
        """Games end screen"""
        if self.running and self.hero.dead: # Game is over and player has not died
            self.screen.fill(LIGHT_GREEN[0])
            self.write("GAME OVER!!", WHITE, 60, WIDTH / 2, HEIGHT / 5)
            self.write("Press any key to play again", WHITE, 25, WIDTH / 2, HEIGHT / 2)
            pygame.display.update()
            self.wait() # Waits for user input

    def level_transition(self):
        """Level transistion screen"""
        if self.running: # Game has not ended
            self.screen.fill(LIGHT_GREEN[0])
            self.write("Level " + str(self.level), WHITE, 60, WIDTH / 2, HEIGHT / 2)
            pygame.display.update()
            time.sleep(1.5) # Stops the program for 1.5 seconds

    def difficulty_screen(self):
        """Lets the player pick the game difficulty"""
        self.screen.fill(LIGHT_GREEN[0]) # Makes the windows background green
        self.write("Select The Game Difficulty!!", WHITE, 45, WIDTH / 2, HEIGHT / 5)
        self.god_mode = Button(LIGHT_GREEN[1], WIDTH / 2, HEIGHT / 3, 200, 50, "God Mode", self)
        self.normal_mode = Button(LIGHT_GREEN[1], WIDTH / 2, HEIGHT / 2, 200, 50, "Normal", self)
        waiting = True
        while waiting:
            self.god_mode.draw(self.screen)
            self.normal_mode.draw(self.screen)
            pygame.display.update()
            for event in pygame.event.get():
                position = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.god_mode.mouse_over(position):
                        self.difficulty = "god"
                        waiting = False
                    elif self.normal_mode.mouse_over(position):
                        self.difficulty = "normal"
                        waiting = False
                
                if event.type == pygame.MOUSEMOTION:
                    if self.god_mode.mouse_over(position):
                        self.god_mode.colour = LIGHT_GREEN[2]
                    else:
                        self.god_mode.colour = LIGHT_GREEN[1]
                    if self.normal_mode.mouse_over(position):
                        self.normal_mode.colour = LIGHT_GREEN[2]
                    else:
                        self.normal_mode.colour = LIGHT_GREEN[1]

    def wait(self):
        """Waits for user input"""
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                # Checks if the player quit
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                # Checks if the user pressed down a key
                if event.type == pygame.KEYUP:
                    waiting = False


game = Game() # Creates game object
game.start_screen()
game.difficulty_screen()
# Continues creating new games until the game.running variable is set to False
while game.running:
    game.level_transition()
    game.new()
    game.end_screen()
pygame.quit()