""" main game loop"""
import pygame

# Initialize Pygame
pygame.init()

# Set up the display
window_size = (400, 300)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Red Dot Game")

# Set up the colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Set up the rectangle (static for this example)
rect_pos = (150, 100)
rect_size = (100, 50)
rectangle = pygame.Rect(rect_pos, rect_size)

# Create surfaces for masks
dot_radius = 10
dot_surface = pygame.Surface((dot_radius*2, dot_radius*2), pygame.SRCALPHA)
pygame.draw.circle(dot_surface, RED, (dot_radius, dot_radius), dot_radius)
dot_mask = pygame.mask.from_surface(dot_surface)

rect_surface = pygame.Surface(rect_size)
rect_surface.fill(GREEN)
rect_mask = pygame.mask.from_surface(rect_surface)

# Game loop
running = True
input_vector = [0, 0]
dot_pos = [window_size[0] // 2, window_size[1] // 2]
speed = 0.01
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
    pygame.draw.circle(screen, RED, dot_pos, dot_radius)

    # Collision detection using masks
    offset_x = rect_pos[0] - dot_pos[0] + dot_radius
    offset_y = rect_pos[1] - dot_pos[1] + dot_radius

    # Check for collision
    if dot_mask.overlap(rect_mask, (offset_x, offset_y)):

        # Draw the rectangle in red if there is a collision
        pygame.draw.rect(screen, RED, rectangle)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
