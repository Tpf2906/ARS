"""module containing code to generate a maze and draw it on the screen"""

from typing import List

import random
import pygame

from config.maze_config import NUM_ROOMS, ROOM_SIZE, BLACK, NUM_LANDMARKS, LANDMARK_COLOR

pygame.font.init()
FONT = pygame.font.SysFont('Arial', 12)

class Maze:
    """Class to generate and draw a maze."""
    def __init__(self, width, height, cell_size, grid=None, rect_list=None, landmarks=None):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.cols = self.width // self.cell_size
        self.rows = self.height // self.cell_size
        
        if grid is None:
            self.grid = [[1 for _ in range(self.cols)] for _ in range(self.rows)]
            self.dfs(1, 1)
            self.create_rooms(NUM_ROOMS, ROOM_SIZE)
        else:
            self.grid = grid

        if rect_list is None:
            self.rect_list = []
            self.make_rects()
        else:
            self.rect_list = rect_list

        if landmarks is None:
            self.landmarks = []
            self.add_landmark(NUM_LANDMARKS)
        else:
            self.landmarks = landmarks

        self.dfs(1, 1)
        self.create_rooms(NUM_ROOMS, ROOM_SIZE)
        self.make_rects()
        self.add_landmark(NUM_LANDMARKS)

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

    def create_rooms(self, num_rooms, room_size):
        """Create rooms in the maze by clearing specified areas."""
        for _ in range(num_rooms):
            x = random.randint(1, (self.rows - 1) // 2) * 2
            y = random.randint(1, (self.cols - 1) // 2) * 2
            for i in range(-room_size, room_size + 1):
                for j in range(-room_size, room_size + 1):
                    if 1 <= x + i < self.rows - 1 and 1 <= y + j < self.cols - 1:
                        self.grid[x + i][y + j] = 0

    def make_rects(self):
        """Create the rectangles for the maze."""
        for x in range(self.rows):
            for y in range(self.cols):
                if self.grid[x][y] == 1:
                    self.rect_list.append(pygame.Rect(y * self.cell_size, x * self.cell_size, self.cell_size, self.cell_size))#pylint: disable=line-too-long

    def add_landmark(self, landmarks):
        """Add a landmark to the maze."""
        for _ in range(landmarks):
            while True:
                x = random.randint(1, self.rows - 2)
                y = random.randint(1, self.cols - 2)
                if self.grid[x][y] == 0:
                    # Store the center of the landmark
                    center_x = y * self.cell_size + self.cell_size // 2
                    center_y = x * self.cell_size + self.cell_size // 2
                    self.landmarks.append((center_x, center_y))

                    #Set the landmark cell to 2
                    self.grid[x][y] = 2
                    break

    def draw(self, screen):
        """Draw the maze."""
        for rect in self.rect_list:
            pygame.draw.rect(surface=screen, color=BLACK, rect=rect)
        for landmark in self.landmarks:
            pygame.draw.circle(surface=screen, color = LANDMARK_COLOR,
                               center=landmark, radius=self.cell_size // 4)
