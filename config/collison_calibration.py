""" main game loop"""
#pylint: disable=no-member
import pygame
from config.robot_config import ROBOT_RADIUS

# Initialize Pygame
pygame.init()

# Set up the display
window_size = (400, 300)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Collision checker")

# Set up the colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Set up the rectangle (static for this example)
rect_pos = (150, 50)
rect_size = (100, 50)
rectangle = pygame.Rect(rect_pos, rect_size)

# Create surfaces for masks
dot_surface = pygame.Surface((ROBOT_RADIUS*2, ROBOT_RADIUS*2), pygame.SRCALPHA)
pygame.draw.circle(dot_surface, RED, (ROBOT_RADIUS, ROBOT_RADIUS), ROBOT_RADIUS)
dot_mask = pygame.mask.from_surface(dot_surface)

rect_surface = pygame.Surface(rect_size)
rect_surface.fill(GREEN)
rect_mask = pygame.mask.from_surface(rect_surface)

def run_calibration():
    """Run this function to report the mask pixel at which the collision occurs.
       manualy move the robot to collide with the rectangle and print the collision coordinates."""
    # Game loop
    running = True
    input_vector = [0, 0]
    dot_pos = [window_size[0] // 2, window_size[1] // 2]
    speed = 0.01
    curr_col_coord = None
    prev_col_coord = None
    while running:
        # Get the list of keys pressed
        keys = pygame.key.get_pressed()

        # Update the input vector based on the keys pressed
        input_vector[0] = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        input_vector[1] = keys[pygame.K_DOWN] - keys[pygame.K_UP]

        # Move the dot
        dot_pos[0] += input_vector[0] * speed
        dot_pos[1] += input_vector[1] * speed

        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the screen with white
        screen.fill(WHITE)

        # Draw the rectangle
        pygame.draw.rect(screen, GREEN, rectangle)

        # Draw the red dot
        pygame.draw.circle(screen, RED, dot_pos, ROBOT_RADIUS)

        # Collision detection using masks
        offset_x = rect_pos[0] - dot_pos[0] + ROBOT_RADIUS
        offset_y = rect_pos[1] - dot_pos[1] + ROBOT_RADIUS

        # Check for collision
        new_col_coord = dot_mask.overlap(rect_mask, (offset_x, offset_y))
        if new_col_coord:
            # Draw the rectangle in red if there is a collision
            pygame.draw.rect(screen, RED, rectangle)

        prev_col_coord = curr_col_coord
        curr_col_coord = new_col_coord
        if curr_col_coord != prev_col_coord and prev_col_coord is None:
            # Print the collision coordinates, only if they change
            print(f"Collision at {new_col_coord}, rectangle is at {rect_pos}, dot is at {tuple(dot_pos)}")#pylint: disable=line-too-long

            # update collision coordinates
            curr_col_coord = new_col_coord

        # Update the display
        pygame.display.flip()
