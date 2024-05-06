"""This module contains the configuration for the maze game."""
import pygame

pygame.init() # pylint: disable=no-member

WIDTH, HEIGHT = 1000, 800 #1200, 900
CELL_SIZE = 40
NUM_ROOMS = 8
ROOM_SIZE = 3
NUM_LANDMARKS = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LANDMARK_COLOR = (0, 0, 112)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
FONT = pygame.font.SysFont('Arial', 18)
