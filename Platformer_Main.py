# Platformer main file

# Importing required modules
import pygame
import random
from Platformer_Settings import *
from Platformer_Sprites import *
from Platformer_Camera import *

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

    def new(self):
        """Starts new game"""
        self.all_sprites = pygame.sprite.Group()
        self.environment = pygame.sprite.Group()
        self.arrows = pygame.sprite.Group()
        self.ladders = pygame.sprite.Group()
        #self.all_sprites.add(self.hero)
        for row, tiles in enumerate(self.map.tile_map):
            for column, tile in enumerate(tiles):
                if tile != ".":
                    if tile == "P":
                        self.hero_x, self.hero_y = column, row
                    elif tile == "la":
                        self.ladder = Ladder(column, row, self)
                    else:
                        self.environment_block = Environment(column, row, tile, self)
        self.camera = Camera(self.map.width, self.map.height)
        self.hero = Hero(self.hero_x, self.hero_y, self)
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
        self.all_sprites.update()
        self.camera.update(self.hero)

    def events(self):
        """Game loops events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.hero.do_jump()

    def paint(self):
        """Draws onto the window"""
        self.screen.fill(SKY_BLUE)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.move_sprite(sprite))
        pygame.display.update()

game = Game()
while game.running:
    game.new()
pygame.quit()