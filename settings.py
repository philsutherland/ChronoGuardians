import pygame
import sys
import random


# Constants for the game
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
BLOCK_SIZE = 30
HEALTH_BAR_HEIGHT = 5
FPS = 60


# Colors
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (28, 70, 87)
DARK_RED = (87, 28, 28)
DARK_GREEN = (28, 87, 33)
DARK_PURPLE = (87, 28, 87)
DARK_ORANGE = (204, 85, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 100)
PURPLE = (160, 32, 240)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

ENEMY_COLORS = [RED, YELLOW, MAGENTA, CYAN, ORANGE]

# Pathway (list of (x, y) tuples)
pathway = [
    (301, 270),
    (301, 450),
    (181, 450),
    (181, 630),
    (481, 630),
    (481, 810),
    (601, 810),
    (601, 870)
]
