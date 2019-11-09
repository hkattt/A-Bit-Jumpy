# Platformer main file

# Importing required modules
import pygame
import random
from Platformer_Settings import *
from Platformer_Sprites import *
from Platformer_Camera import *
from Platformer_Display import *

class Game():
    def __init__(self):
        """Initialize game window and pygame"""
        pygame.init() 
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Platformer")
        self.clock = pygame.time.Clock()
        self.running = True
        self.load_map()

    def load_map(self):
        self.map = Map()
 
    def new(self ):
        """Starts new game"""
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
        for row, tiles in enumerate(self.map.tile_map):
            for column, tile in enumerate(tiles):
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
                        self.fly = Fly(column, row, self)
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
        if current - self.enemy_timer > ENEMY_SPAWN + random.choice([-1000, 0, 1000, 3000]):
            self.enemy_timer = current 
            for spawner in self.spawners:
                self.enemy = spawner.create_enemy()
                if self.enemy != None:
                    spawner.orcs.append(self.enemy)

        self.all_sprites.update()
        self.display_objects.update()
        self.camera.update(self.hero)

    def events(self):
        """Game loops events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

        if self.hero.dead == True:
            self.playing = False
            self.running = False

    def paint(self):  
        """Draws onto the window"""
        self.screen.fill(SKY_BLUE)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.move_sprite(sprite))
        for sprite in self.display_objects:
            self.screen.blit(sprite.image, sprite)
        self.coin_display.write(str(self.hero.coins), 45, self.coin_display.position.x + 64, self.coin_display.position.y + 8)
        pygame.display.update()

game = Game()
while game.running:
    game.new()
pygame.quit()