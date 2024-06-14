"""module for handling the controls of the game though various methods."""
import pygame
from maze_game import MazeGame

def human_controls(game: MazeGame):
    """control the game with the keyboard."""
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #pylint: disable=no-member
                running = False

        keys = pygame.key.get_pressed()
        vr_input, vl_input = game.handle_controls(keys)
        game.step(vr_input, vl_input)

    pygame.quit() #pylint: disable=no-member

def ai_controls(game: MazeGame, ai):
    """control the game with the ai."""
    running = True

    while running:
        vr_input, vl_input = ai.get_action(game.robot)
        game.step(vr_input, vl_input)
