"""robot.py: A simple robot class that can move around a maze."""
import math
import pygame
import numpy as np

from maze_config import CELL_SIZE, WIDTH, HEIGHT, FONT, BLUE
from robot_config import (ROBOT_RADIUS, ROBOT_COLOR, SENSOR_COLOR, SENSOR_COLOR_LANDMARK,
                          TEXT_COLOR, NUM_SENSORS, SENSOR_MAX_DISTANCE)
from kalman_filter import KalmanFilter
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
        self.estimated_positions = [(self.x, self.y)]# Store estimated positions for drawing later

        #TODO: (Tiago) please fix the naming convention
        #pylint: disable=invalid-name
        # Initialize the Kalman filter
        A = np.eye(3)
        B = np.zeros((3, 2))
        C = None  # Will be defined dynamically in the Kalman filter class
        Q = np.diag([0.01, 0.01, 0.01])
        R = np.diag([0.1, 0.1] * len(maze.landmarks))
        x = np.array([self.x, self.y, self.angle])
        P = np.eye(3)

        self.kalman_filter = KalmanFilter(A, B, C, Q, R, x, P)
        #pylint: enable=invalid-name

    def _make_mask(self):
        """Create a mask for the robot."""
        dot_surface = pygame.Surface((ROBOT_RADIUS * 2, ROBOT_RADIUS * 2), pygame.SRCALPHA) #pylint: disable=no-member
        pygame.draw.circle(dot_surface, SENSOR_COLOR, (ROBOT_RADIUS, ROBOT_RADIUS), ROBOT_RADIUS)
        dot_mask = pygame.mask.from_surface(dot_surface)

        return dot_mask

    def update_sensors(self, angle=0):
        """Update the sensor readings based on the robot's current position."""
        for i in range(NUM_SENSORS):
            sensor_angle = self.angle + i * (2 * math.pi / NUM_SENSORS)
            self.sensors[i] = self._raycast(sensor_angle + angle, 'wall')


    def landmark_raycast(self, screen): #pylint: disable=missing-function-docstring
        #TODO: (Lisa) add a doc string, describe the method
        for (lx, ly) in self.maze.landmarks:
            angle = math.atan2(ly - self.y, lx - self.x)
            total_distance = math.sqrt((lx - self.x) ** 2 + (ly - self.y) ** 2)
            is_obstructed = False

            # Initialize ray's position to this starting point on the robot's circumference
            x, y = self.x, self.y

            # Calculate the unit vector for the ray
            dx = math.cos(angle)
            dy = math.sin(angle)

            for _ in range(int(total_distance)):
                x += dx
                y += dy
                grid_x, grid_y = int(x // CELL_SIZE), int(y // CELL_SIZE)

                # Check if the ray has hit a wall in the maze
                if grid_y >= len(self.maze.grid)\
                    or grid_x >= len(self.maze.grid[0])\
                    or self.maze.grid[grid_y][grid_x] == 1:
                    is_obstructed = True
                    break

            if not is_obstructed:
                pygame.draw.line(screen, SENSOR_COLOR_LANDMARK, (self.x, self.y), (lx, ly), 2)
                self._draw_sensor_text(screen, total_distance, angle)

    def _raycast(self, angle, obstacle_type):
        """
        Cast a ray from the edge of the robot at a given angle.
        Return the distance to the obstacle.
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

        if obstacle_type == "wall":
            # Raycasting loop for walls
            while distance < SENSOR_MAX_DISTANCE:
                x += dx
                y += dy
                distance += 1
                grid_x, grid_y = int(x // CELL_SIZE), int(y // CELL_SIZE)

                # Check if the ray has hit a wall in the maze
                #TODO: (Lisa) this check is used at least three times, abstract to own function
                if grid_y >= len(self.maze.grid)\
                   or grid_x >= len(self.maze.grid[0])\
                   or self.maze.grid[grid_y][grid_x] == 1:
                    return distance

            return SENSOR_MAX_DISTANCE

        if obstacle_type == 'landmark':
            # Raycasting loop for landmarks
            for (lx, ly) in self.maze.landmarks:
                l_distance = math.sqrt((lx - self.x) ** 2 + (ly - self.y) ** 2)
                if l_distance < SENSOR_MAX_DISTANCE:
                    dx = (lx - start_x) / l_distance
                    dy = (ly - start_y) / l_distance

                    ray_x, ray_y = start_x, start_y
                    for _ in range(int(l_distance)):
                        ray_x += dx
                        ray_y += dy
                        grid_x, grid_y = int(ray_x // CELL_SIZE), int(ray_y // CELL_SIZE)

                        if grid_y >= len(self.maze.grid)\
                           or grid_x >= len(self.maze.grid[0])\
                           or self.maze.grid[grid_y][grid_x] == 1:
                            return SENSOR_MAX_DISTANCE

                    return l_distance

            return SENSOR_MAX_DISTANCE

    def move_with_diff_drive(self, vl, vr):
        """Move the robot with differential drive control."""
        # Create state vector
        state = [self.x, self.y, self.angle, vl, vr]

        # Update the state
        new_state = motion_with_collision(state, 1, self.maze.rect_list, self.mask)

        # Update the robot's position
        self.x, self.y, self.angle = new_state[0], new_state[1], new_state[2]

        # Add the current position to past positions
        self.past_positions.append((self.x, self.y))

        # Check for collision with the outer edges of the window
        self.x = max(self.x, ROBOT_RADIUS)
        self.y = max(self.y, ROBOT_RADIUS)
        self.x = min(self.x, WIDTH - ROBOT_RADIUS)
        self.y = min(self.y, HEIGHT - ROBOT_RADIUS)

        # Kalman filter predict and correct steps
        control_vector = np.array([vl, vr])
        self.kalman_filter.predict(control_vector)

        # Update measurement_vector with actual landmark data
        measurement_vector = []

        for (lx, ly) in self.maze.landmarks:
            dx = lx - self.x
            dy = ly - self.y
            distance = np.sqrt(dx ** 2 + dy ** 2)
            bearing = np.arctan2(dy, dx) - self.angle
            measurement_vector.extend([bearing, distance])

        measurement_vector = np.array(measurement_vector)

        # Correct step in Kalman filter
        self.kalman_filter.correct(measurement_vector, self.maze.landmarks)

        # Store estimated positions for drawing
        estimated_position = self.kalman_filter.get_state_estimate()
        self.estimated_positions.append((estimated_position[0], estimated_position[1]))


    def draw_path(self, screen):
        """Draw the robot's path on the screen."""
        if len(self.past_positions) > 1:
            pygame.draw.lines(screen, BLUE, False, self.past_positions, 2)  # Draw path in blue

        if len(self.estimated_positions) > 1:
            pygame.draw.lines(screen, (255, 255, 0), False, self.estimated_positions, 2)  # Draw estimated path in yellow pylint: disable=line-too-long

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
            end_x = self.x + sensor_distance * math.cos(sensor_angle) + ROBOT_RADIUS * math.cos(sensor_angle) # pylint: disable=line-too-long
            end_y = self.y + sensor_distance * math.sin(sensor_angle) + ROBOT_RADIUS * math.sin(sensor_angle) # pylint: disable=line-too-long

            # Forward sensor direction check
            if i == 0:  # Assuming forward direction is index 0 after the angle correction
                sensor_color = (255, 0, 255)  # Purple for forward direction
            else:
                sensor_color = SENSOR_COLOR

            pygame.draw.line(screen, sensor_color, (self.x, self.y), (end_x, end_y), 2)
            self._draw_sensor_text(screen, sensor_distance, sensor_angle)
