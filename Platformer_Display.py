# Platformer Display

# Imports required modules
import pygame
# Imports setting file
from Platformer_Settings import *
vector = pygame.math.Vector2
# Find font name
font_name = pygame.font.match_font("times")

class Display(pygame.sprite.Sprite):
    """Display objects parent class"""
    def __init__(self, x, y, game):
        """Initiates display object"""
        self.groups = game.display_objects # Display objects group
        # Initiates sprite class
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.position = vector(int(x * TILE_SIZE), int(y * TILE_SIZE))

class Coin_Count(Display):
    """Players coin display"""
    def __init__(self, x, y, game):
        """Initiates coin display"""
        # Inherits from the parent class
        super().__init__(x, y, game)
        self.load_images()
        self.image = self.coin
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.position

    def load_images(self):
        """Loads in image for coin display"""
        self.coin = pygame.image.load("gold_coin.png")

class Health(Display):
    """Players health display"""
    def __init__(self, x, y, game):
        """Initiates health display"""
        # Inherits from the parent class
        super().__init__(x, y, game)
        self.load_images()
        self.image = self.heart[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.position

    def update(self):
        """Updates the health display"""
        self.animation()

    def animation(self):
        """Animates the health display"""
        # Player has full health
        if self.game.hero.hearts == 3:
            self.image = self.heart[0]
        # Player has half health
        elif self.game.hero.hearts == 2:
            self.image = self.heart[1]
        elif self.game.hero.hearts == 1:
            self.image = self.heart[2]
    
    def load_images(self):
        """Loads in images for health display animation"""
        self.heart = [pygame.image.load("heart_full.png"), pygame.image.load("heart_half.png"), pygame.image.load("heart_empty.png")]

class Key_Display(Display):
    """Levels key display"""
    def __init__(self, x, y, game):
        """Initiates key display object"""
        # Inherits from parent class
        super().__init__(x, y, game)
        self.load_images()
        self.image = self.keys[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.position

    def update(self):
        """Updates key display"""
        self.animation()
    
    def animation(self):
        """Animates key display sprite"""
        # If the player has collected all the keys
        if len(self.game.keys) <= 0:
            self.image = self.keys[1]
    
    def load_images(self):
        """Loads in images for key animation"""
        self.keys = [pygame.image.load("key_empty.png"), pygame.image.load("key_full.png")]