"""robot.py: A simple robot class that can move around a maze."""
import math
import pygame

from maze_config import CELL_SIZE, WIDTH, HEIGHT, FONT, BLUE, NUM_LANDMARKS
from robot_config import (ROBOT_RADIUS, ROBOT_COLOR, SENSOR_COLOR,SENSOR_COLOR_LANDMARK,
                          TEXT_COLOR, NUM_SENSORS, SENSOR_MAX_DISTANCE)

from forward_kin import motion_with_collision

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
        self.mask = self._make_mask()
        self.past_positions = [(self.x, self.y)]

    def _make_mask(self):
        """Create a mask for the robot."""
        dot_surface = pygame.Surface((ROBOT_RADIUS*2, ROBOT_RADIUS*2), pygame.SRCALPHA) #pylint: disable=no-member
        pygame.draw.circle(dot_surface, SENSOR_COLOR, (ROBOT_RADIUS, ROBOT_RADIUS), ROBOT_RADIUS)
        dot_mask = pygame.mask.from_surface(dot_surface)

        return dot_mask

    #TODO: (Jounaid) consider variable framerate based on distance
    def update_sensors(self, angle = 0):
        """Update the sensor readings based on the robot's current position."""
        for i in range(NUM_SENSORS):
            sensor_angle = self.angle + i * (2 * math.pi / NUM_SENSORS)
            self.sensors[i] = self._raycast(sensor_angle + angle)
    

    #TODO: (LISA) check if  the distance is within a certain threshold
    def landmark_raycast(self,screen):
        landmarks = self.maze.landmarks
        start_x = self.x
        start_y = self.y
        for i in range(NUM_LANDMARKS):
            end_x = landmarks[i][0]
            end_y = landmarks[i][1]
            dx = end_x - start_x
            dy = end_y - start_y
            distance = math.sqrt(dx**2 + dy**2)
            angle = math.atan2(dy, dx)
            if distance < SENSOR_MAX_DISTANCE:
                ray_distance = self._raycast(angle)
                #FIX ME
                if (1):#(abs(ray_distance - distance) < 2):
                    pygame.draw.line(screen, SENSOR_COLOR_LANDMARK, (start_x, start_y), (end_x, end_y), 2)
            else:
                break

    def _raycast(self, angle):
        """
        Cast a ray from the edge of the robot at a given angle to return the distance to the wall.
        """
        # Calculate the starting point from the robot's edge in the direction of the angle
        start_x = self.x + ROBOT_RADIUS * math.cos(angle)
        start_y = self.y + ROBOT_RADIUS * math.sin(angle)

        # Initialize ray's position to this starting point on the robot's circumference
        x, y = start_x, start_y
        distance = -1

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
            if grid_y >= len(self.maze.grid) or grid_x >= len(self.maze.grid[0]) or self.maze.grid[grid_y][grid_x] == 1: #pylint: disable=line-too-long
                break

        # Return the total distance from the edge of the robot to the wall
        return distance

    def move_with_diff_drive(self, vl, vr):
        """Move the robot with differential drive control."""

        # create state vector
        state = [self.x, self.y, self.angle, vl, vr]

        # update the state
        new_state = motion_with_collision(state, 1, self.maze.rect_list, self.mask)

        # update the robot's position
        self.x, self.y, self.angle = new_state[0], new_state[1], new_state[2]

        # Add the current position to past positions
        self.past_positions.append((self.x, self.y))

        # check for collision with the outer edges of the window
        self.x = max(self.x, ROBOT_RADIUS)
        self.y = max(self.y, ROBOT_RADIUS)
        self.x = min(self.x, WIDTH - ROBOT_RADIUS)
        self.y = min(self.y, HEIGHT - ROBOT_RADIUS)

    def draw_path(self, screen):
        """Draw the robot's path on the screen."""
        if len(self.past_positions) > 1:
            pygame.draw.lines(screen, BLUE, False, self.past_positions, 2)  # Draw path in blue

    def _draw_sensor_text(self, screen, sensor_distance, angle, distance_multiplier=1.1):
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
        """Draw the robot on the screen."""
        pygame.draw.circle(screen, ROBOT_COLOR, (int(self.x), int(self.y)), ROBOT_RADIUS)

        # Sensor that should be highlighted is the one aligned with the angle
        for i, sensor_distance in enumerate(self.sensors):
            sensor_angle = self.angle + i * (2 * math.pi / NUM_SENSORS)
            end_x = self.x + sensor_distance * math.cos(sensor_angle) + ROBOT_RADIUS * math.cos(sensor_angle) #pylint: disable=line-too-long
            end_y = self.y + sensor_distance * math.sin(sensor_angle) + ROBOT_RADIUS * math.sin(sensor_angle) #pylint: disable=line-too-long
            # Forward sensor direction check
            if i == 0:  # Assuming forward direction is index 0 after the angle correction
                sensor_color = (255, 0, 255)  # Purple for forward direction
            else:
                sensor_color = SENSOR_COLOR

            pygame.draw.line(screen, sensor_color, (self.x, self.y), (end_x, end_y), 2)
            self._draw_sensor_text(screen, sensor_distance, sensor_angle)

  
