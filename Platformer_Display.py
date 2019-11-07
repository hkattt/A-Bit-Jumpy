# Platformer Display

import pygame
from Platformer_Settings import *
vector = pygame.math.Vector2
font_name = pygame.font.match_font("times")

class Display(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        """Initiates display"""
        self.groups = game.all_sprites, game.display_objects
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
    
    def update(self):
        print("hello")
        self.draw(str(self.game.hero.coins), 60, self.position.x, self.position.y)

    def draw(self, score, size, x, y):
        """Draws the players coin count onto the screen"""
        coin_count = pygame.font.Font(font_name, size)
        text_surface = coin_count.render(score, True, BLACK)
        text_rect = text_surface.get_rect()
        text_rect.x, text_rect.y = x, y
        self.game.screen.blit(text_surface, text_rect)

    def load_images(self):
        """Loads in images for coin display"""
        self.coin = pygame.image.load("gold_coin.png")
