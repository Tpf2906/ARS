"""robot.py: A simple robot class that can move around a maze."""
import math
import pygame

#TODO: create a confg file to store all the constants
from maze import CELL_SIZE, WIDTH, HEIGHT, FONT


ROBOT_RADIUS = CELL_SIZE // 3
ROBOT_COLOR = (255, 0, 0) 
SENSOR_COLOR = (0, 255, 0) 
SENSOR_COLOR_FORWARD = (0, 0, 255)
TEXT_COLOR = (255, 255, 0) 
TEXT_COLOR_SPEED = (0, 0, 0) 
NUM_SENSORS = 12  
SENSOR_MAX_DISTANCE = WIDTH  
ROBOT_SPEED = 2

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
        self.prev_x, self.prev_y = 0, 0
        self.speed = 0

    #TODO: (@Jounaid) consider variable framerate based on distance
    def update_sensors(self, angle = 0):
        """Update the sensor readings based on the robot's current position."""
        for i in range(NUM_SENSORS):
            sensor_angle = math.radians(self.angle + i * (360 / NUM_SENSORS))
            self.sensors[i] = self._raycast(sensor_angle + angle)
            
    #TODO: (@Lisa) modifying 
    def _raycast(self, angle):
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
        print("Debug.robot._raycast: distance: ", distance, "x: ", grid_x, "y: ", grid_y, "start_x: ", start_x, "start_y: ", start_y)
        return distance

    #TODO: (Jounaid) write alternative for differential drive control
    def move(self, direction):
        self.prev_x, self.prev_y = self.x, self.y
        
        """Move the robot in the given direction."""
        if direction == 'UP':
            self.y -= ROBOT_SPEED
            self.angle = 270
        elif direction == 'DOWN':
            self.y += ROBOT_SPEED
            self.angle = 90
        elif direction == 'LEFT':
            self.x -= ROBOT_SPEED
            self.angle = 180
        elif direction == 'RIGHT':
            self.x += ROBOT_SPEED
            self.angle = 0
        elif direction == 'RIGHT' & direction == 'UP':
            self.y -= ROBOT_SPEED
            self.x += ROBOT_SPEED
            self.angle = 0

        self.x = max(self.x, ROBOT_RADIUS)
        self.y = max(self.y, ROBOT_RADIUS)
        self.x = min(self.x, WIDTH - ROBOT_RADIUS)
        self.y = min(self.y, HEIGHT - ROBOT_RADIUS)

        self.speed = ROBOT_SPEED if (self.x != self.prev_x or self.y != self.prev_y) else 0


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
        pygame.draw.circle(screen, ROBOT_COLOR, (int(self.x), int(self.y)), ROBOT_RADIUS)

        # Sensor that should be highlighted is the one aligned with the angle
        for i, sensor_distance in enumerate(self.sensors):
            sensor_angle = math.radians(self.angle + i * (360 / NUM_SENSORS))
            end_x = self.x + sensor_distance * math.cos(sensor_angle) + ROBOT_RADIUS * math.cos(sensor_angle)
            end_y = self.y + sensor_distance * math.sin(sensor_angle) + ROBOT_RADIUS * math.sin(sensor_angle)
            
            # Forward sensor direction check
            if i == 0:  # Assuming forward direction is index 0 after the angle correction
                sensor_color = (255, 0, 255)  # White for forward direction
            else:
                sensor_color = SENSOR_COLOR

            pygame.draw.line(screen, sensor_color, (self.x, self.y), (end_x, end_y), 2)
            self.draw_sensor_text(screen, sensor_distance, sensor_angle)

