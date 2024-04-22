"""This module contains the configuration for the maze game."""
import pygame

pygame.init() # pylint: disable=no-member

WIDTH, HEIGHT = 1500, 1200
CELL_SIZE = 40
NUM_ROOMS = 8
ROOM_SIZE = 3
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.SysFont('Arial', 12)
