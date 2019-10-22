# Map loader and Camera

import pygame
from Platformer_Settings import *

class Map():
    def __init__(self):
        self.tile_map = []
        for line in open("Platformer_Map.txt"):
            self.tile_map.append(line)
    
        self.tile_width = len(self.tile_map[0])
        self.tile_height = len(self.tile_map)
        self.width = self.tile_width * TILE_SIZE
        self.height = self.tile_height * TILE_SIZE

class Camera():
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def move_sprite(self, sprite):
        sprite.rect.move(self.camera.topleft)

    def update(self):
        pass


