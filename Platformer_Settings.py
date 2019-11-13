# Platformer game settings

# Game window size
WIDTH = 1024 # 32 * 32
HEIGHT = 512 # 32 * 16

TILE_SIZE = 64
GRID_WIDTH = WIDTH / TILE_SIZE
GRID_HEIGHT = HEIGHT / TILE_SIZE

ENEMY_SPAWN = 10000

# Colours and FPS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_GREEN = [(152, 255, 152), (152, 215, 152), (40, 170, 40)]
SKY_BLUE = (135,206,235)
GREY = (211, 211, 211)
FPS = 40

# Hero attributes
ACC = 0.2
FRIC = -0.05

# Orc attributes
ORC_ACC = 0.2
ORC_FRIC = -0.1
