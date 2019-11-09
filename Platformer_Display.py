# Platformer Display

import pygame
from Platformer_Settings import *
vector = pygame.math.Vector2
font_name = pygame.font.match_font("times")

class Display(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        """Initiates display"""
        self.groups = game.display_objects
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.position = vector(int(x * TILE_SIZE), int(y * TILE_SIZE))

class Coin_Count(Display):
    def __init__(self, x, y, game):
        """Initiates health from parent class"""
        super().__init__(x, y, game)
        self.load_images()
        self.image = self.coin
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.position
    
    def write(self, score, size, x, y):
        """Draws the players coin count onto the screen"""
        coin_count = pygame.font.Font(font_name, size)
        text_surface = coin_count.render(score, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.x, text_rect.y = x, y
        self.game.screen.blit(text_surface, text_rect)

    def load_images(self):
        """Loads in images for coin display"""
        self.coin = pygame.image.load("gold_coin.png")

class Health(Display):
    def __init__(self, x, y, game):
        """Initiates health display"""
        super().__init__(x, y, game)
        self.load_images()
        self.image = self.heart[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.position

    def update(self):
        self.animation()

    def animation(self):
        if self.game.hero.hearts == 3:
            self.image = self.heart[0]
        elif self.game.hero.hearts == 2:
            self.image = self.heart[1]
        elif self.game.hero.hearts == 1:
            self.image = self.heart[2]
    
    def load_images(self):
        self.heart = [pygame.image.load("heart_full.png"), pygame.image.load("heart_half.png"), pygame.image.load("heart_empty.png")]

class Key_Display(Display):
    def __init__(self, x, y, game):
        """Initiates key display object"""
        super().__init__(x, y, game)
        self.load_images()
        self.image = self.keys[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.position

    def update(self):
        self.animation()
    
    def animation(self):
        if len(self.game.keys) <= 0:
            self.image = self.keys[1]
    
    def load_images(self):
        self.keys = [pygame.image.load("key_empty.png"), pygame.image.load("key_full.png")]