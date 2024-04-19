"""module containing code to generate a maze and draw it on the screen"""
import random
import pygame

# Global constants
WIDTH, HEIGHT = 1000, 800
CELL_SIZE = 40
NUM_ROOMS = 8
ROOM_SIZE = 1
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#TODO: this should probably be in the main
pygame.font.init()
FONT = pygame.font.SysFont('Arial', 12)

class Maze:
    """Class to generate and draw a maze."""
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.cols = self.width // self.cell_size
        self.rows = self.height // self.cell_size
        self.grid = [[1 for _ in range(self.cols)] for _ in range(self.rows)]

    def dfs(self, start_x, start_y):
        """Generate the maze."""
        stack = [(start_x, start_y)]
        self.grid[start_x][start_y] = 0
        directions = [0, 1, 2, 3]  # Directions: 0-North, 1-East, 2-South, 3-West

        while stack:
            cx, cy = stack[-1]
            random.shuffle(directions)
            moved = False

            for direction in directions:
                nx, ny = cx, cy
                if direction == 0:
                    nx -= 2
                elif direction == 1:
                    ny += 2
                elif direction == 2:
                    nx += 2
                elif direction == 3:
                    ny -= 2

                if 1 <= nx < self.rows - 1 and 1 <= ny < self.cols - 1 and self.grid[nx][ny] == 1:
                    self.grid[cx + (nx - cx) // 2][cy + (ny - cy) // 2] = 0
                    self.grid[nx][ny] = 0
                    stack.append((nx, ny))
                    moved = True
                    break

            if not moved:
                stack.pop()

    #FIXME: (@Tiago) rooms can remove the wall on the edge of the maze, they shouldn't
    def create_rooms(self, num_rooms, room_size):
        """Create rooms in the maze by clearing specified areas."""
        for _ in range(num_rooms):
            x = random.randint(1, (self.rows - 1) // 2) * 2
            y = random.randint(1, (self.cols - 1) // 2) * 2
            for i in range(-room_size, room_size + 1):
                for j in range(-room_size, room_size + 1):
                    if 1 <= x + i < self.rows - 1 and 1 <= y + j < self.cols - 1:
                        self.grid[x + i][y + j] = 0

    def draw(self, screen):
        """Draw the maze."""
        for x in range(self.rows):
            for y in range(self.cols):
                color = WHITE if self.grid[x][y] == 0 else BLACK
                pygame.draw.rect(screen, color, (y * self.cell_size, x * self.cell_size, self.cell_size, self.cell_size)) #pylint: disable=line-too-long
