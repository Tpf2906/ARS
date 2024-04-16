import pygame
import random

# Global constants for configuration
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
NUM_ROOMS = 10
ROOM_SIZE = 1
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Maze:
    """A class for generating and managing a maze."""
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.cols = self.width // self.cell_size
        self.rows = self.height // self.cell_size
        self.grid = [[1 for _ in range(self.cols)] for _ in range(self.rows)]

    def dfs(self, start_x, start_y):
        """Generate the maze using the Depth-First Search algorithm."""
        stack = [(start_x, start_y)]
        self.grid[start_x][start_y] = 0
        directions = [0, 1, 2, 3]  # Directions: 0-North, 1-East, 2-South, 3-West

        while stack:
            cx, cy = stack[-1]
            random.shuffle(directions)
            moved = False

            for direction in directions:
                nx, ny = cx, cy
                if direction == 0: nx -= 2
                elif direction == 1: ny += 2
                elif direction == 2: nx += 2
                elif direction == 3: ny -= 2

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
            x = random.randint(1, self.rows - 2)
            y = random.randint(1, self.cols - 2)
            for i in range(-room_size, room_size + 1):
                for j in range(-room_size, room_size + 1):
                    if 1 <= x + i < self.rows - 1 and 1 <= y + j < self.cols - 1:
                        self.grid[x + i][y + j] = 0

    def draw(self, screen):
        """Draw the maze on the Pygame screen."""
        for x in range(self.rows):
            for y in range(self.cols):
                color = WHITE if self.grid[x][y] == 0 else BLACK
                pygame.draw.rect(screen, color, (y * self.cell_size, x * self.cell_size, self.cell_size, self.cell_size))

class MazeGame:
    """A class to handle game initialization and the main game loop."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.maze = Maze(WIDTH, HEIGHT, CELL_SIZE)
        self.maze.dfs(1, 1)
        self.maze.create_rooms(NUM_ROOMS, ROOM_SIZE)

    def run(self):
        """Run the main game loop."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(BLACK)
            self.maze.draw(self.screen)
            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    game = MazeGame()
    game.run()
