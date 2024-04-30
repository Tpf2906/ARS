"""This module contains the configuration for the maze game."""
import pygame

pygame.init() # pylint: disable=no-member

WIDTH, HEIGHT = 1200, 900
CELL_SIZE = 40
NUM_ROOMS = 8
ROOM_SIZE = 3
NUM_LANDMARKS = 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
FONT = pygame.font.SysFont('Arial', 18)
