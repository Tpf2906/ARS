import pygame
import random
import math

# Global constants
WIDTH, HEIGHT = 1000, 800
CELL_SIZE = 40
NUM_ROOMS = 8
ROOM_SIZE = 1
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Robot
ROBOT_RADIUS = CELL_SIZE // 3
ROBOT_COLOR = (255, 0, 0) 
SENSOR_COLOR = (0, 255, 0) 
TEXT_COLOR = (255, 255, 0) 
NUM_SENSORS = 12  
SENSOR_MAX_DISTANCE = WIDTH  
ROBOT_SPEED = 2  

pygame.font.init()
FONT = pygame.font.SysFont('Arial', 12)

class Maze:
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
                pygame.draw.rect(screen, color, (y * self.cell_size, x * self.cell_size, self.cell_size, self.cell_size))

class Robot:
    """Robot with sensors to navigate and sense the maze."""

    def __init__(self, maze, start_pos):
        """
        Initialize the robot.
        :param maze: Maze object which the robot will navigate.
        :param start_pos: Tuple (x, y) for the starting position of the robot.
        """
        self.maze = maze
        self.x, self.y = start_pos
        self.sensors = [0] * NUM_SENSORS
        self.angle = 0

    def update_sensors(self):
        """Update the sensor readings based on the robot's current position."""
        for i in range(NUM_SENSORS):
            sensor_angle = math.radians(self.angle + i * (360 / NUM_SENSORS))
            self.sensors[i] = self.raycast(sensor_angle)

    def raycast(self, angle):
        """
        Cast a ray from the edge of the robot at a given angle to return the distance to the wall.
        """
        # Calculate the starting point from the robot's edge in the direction of the angle
        start_x = self.x + ROBOT_RADIUS * math.cos(angle)
        start_y = self.y + ROBOT_RADIUS * math.sin(angle)

        # Initialize ray's position to this starting point on the robot's circumference
        x, y = start_x, start_y
        distance = 0

        # Calculate the unit vector for the ray
        dx = math.cos(angle)
        dy = math.sin(angle)

        # Raycasting loop
        while distance < SENSOR_MAX_DISTANCE:
            x += dx
            y += dy
            distance += 1
            grid_x, grid_y = int(x // CELL_SIZE), int(y // CELL_SIZE)

            # Check if the ray has hit a wall in the maze
            if grid_y >= len(self.maze.grid) or grid_x >= len(self.maze.grid[0]) or self.maze.grid[grid_y][grid_x] == 1:
                break

        # Return the total distance from the edge of the robot to the wall
        return distance

    def move(self, direction):
        """Move the robot in the given direction."""
        if direction == 'UP':
            self.y -= ROBOT_SPEED
        elif direction == 'DOWN':
            self.y += ROBOT_SPEED
        elif direction == 'LEFT':
            self.x -= ROBOT_SPEED
        elif direction == 'RIGHT':
            self.x += ROBOT_SPEED

        self.x = max(self.x, ROBOT_RADIUS)
        self.y = max(self.y, ROBOT_RADIUS)
        self.x = min(self.x, WIDTH - ROBOT_RADIUS)
        self.y = min(self.y, HEIGHT - ROBOT_RADIUS)
        
    def draw_sensor_text(self, screen, sensor_distance, angle, distance_multiplier=1.1):
        """
        Draw the sensor distance reading as text on the screen.
        :param screen: Pygame screen object to draw the text.
        :param sensor_distance: Distance reading from the sensor.
        :param angle: The angle of the sensor in radians.
        :param distance_multiplier: How far from the robot the text should appear.
        """
        end_x = self.x + sensor_distance * math.cos(angle) * distance_multiplier
        end_y = self.y + sensor_distance * math.sin(angle) * distance_multiplier
        text_surface = FONT.render(str(int(sensor_distance)), True, TEXT_COLOR)
        screen.blit(text_surface, (end_x, end_y))


    def draw(self, screen):
        """Draw the robot, its direction, and its sensors on the screen."""
        # Calculate the direction line end point based on the current angle
        direction_x = self.x + ROBOT_RADIUS * math.cos(math.radians(self.angle))
        direction_y = self.y + ROBOT_RADIUS * math.sin(math.radians(self.angle))
        
        pygame.draw.circle(screen, ROBOT_COLOR, (int(self.x), int(self.y)), ROBOT_RADIUS)
        pygame.draw.line(screen, ROBOT_COLOR, (self.x, self.y), (direction_x, direction_y), 2)

        # Draw the sensors as lines
        for i, sensor_distance in enumerate(self.sensors):
            sensor_angle = math.radians(self.angle + i * (360 / NUM_SENSORS))
            end_x = self.x + sensor_distance * math.cos(sensor_angle) + ROBOT_RADIUS * math.cos(sensor_angle)
            end_y = self.y + sensor_distance * math.sin(sensor_angle) + ROBOT_RADIUS * math.sin(sensor_angle)
            pygame.draw.line(screen, SENSOR_COLOR, (self.x, self.y), (end_x, end_y))
            self.draw_sensor_text(screen, sensor_distance, sensor_angle)


class MazeGame:
    """Handle game initialization and the main game loop."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.maze = Maze(WIDTH, HEIGHT, CELL_SIZE)
        self.maze.dfs(1, 1)
        self.maze.create_rooms(NUM_ROOMS, ROOM_SIZE)
        self.robot = Robot(self.maze, (CELL_SIZE * 1.5, CELL_SIZE * 1.5))  # Starting the robot in the first cell
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False
        
    def run(self):
        """Run the main game loop."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.moving_up = True
                    elif event.key == pygame.K_DOWN:
                        self.moving_down = True
                    elif event.key == pygame.K_LEFT:
                        self.moving_left = True
                    elif event.key == pygame.K_RIGHT:
                        self.moving_right = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.moving_up = False
                    elif event.key == pygame.K_DOWN:
                        self.moving_down = False
                    elif event.key == pygame.K_LEFT:
                        self.moving_left = False
                    elif event.key == pygame.K_RIGHT:
                        self.moving_right = False

            # Move the robot
            if self.moving_up:
                self.robot.move('UP')
            if self.moving_down:
                self.robot.move('DOWN')
            if self.moving_left:
                self.robot.move('LEFT')
            if self.moving_right:
                self.robot.move('RIGHT')

            self.screen.fill(BLACK)
            self.maze.draw(self.screen)
            self.robot.update_sensors()
            self.robot.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = MazeGame()
    game.run()