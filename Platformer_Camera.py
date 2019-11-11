# Map loader and Camera

# Imports required modules
import pygame
# Imports other game files
from Platformer_Settings import *
from Platformer_Map import *

class Map():
    """Map object"""
    def __init__(self, level):
        """Initializes Map and creates map list"""
        self.tile_map = []
        # Creates map for desired level
        for line in tile_map[level - 1]:
            self.tile_map.append(line)
    
        self.tile_width = len(self.tile_map[0])
        self.tile_height = len(self.tile_map)
        self.width = self.tile_width * TILE_SIZE
        self.height = self.tile_height * TILE_SIZE

class Town_Map():
    """Town object"""
    def __init__(self):
        """Initiates Town and creates town list"""
        self.tile_town = []
        # Creates town
        for line in town_map:
            self.tile_town.append(line)
        
        self.tile_width = len(self.tile_town[0])
        self.tile_height = len(self.tile_town)
        self.width = self.tile_width * TILE_SIZE
        self.height = self.tile_height * TILE_SIZE

class Camera():
    """Camera object"""
    def __init__(self, width, height):
        """Initializes camera"""
        # Cameras size
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def move_sprite(self, sprite):
        """Moves sprite objects relative to the cameras position"""
        return sprite.rect.move(self.camera.topleft)

    def update(self, sprite):
        """Moves the camera, which will follow a chosen sprite"""
        x = -sprite.rect.x + int(WIDTH / 2)
        y = -sprite.rect.y + int(HEIGHT / 2)
        
        # prevents camera from moving outside of the map
        x = min(0, x) # left side limit
        y = min(0, y) # top side limit
        x = max(-(self.width - WIDTH), x) # right side limit
        y = max(-(self.height - HEIGHT), y) # bottom side limit
        self.camera = pygame.Rect(x, y, self.width, self.height)