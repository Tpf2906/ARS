""" main.py used to run the game """
# disabling pylint no-member error for pygame
# pylint: disable=no-member
import pygame
import random

from maze import Maze
from config.maze_config import WIDTH, HEIGHT, CELL_SIZE, WHITE, FONT
from robot import Robot



class MazeGame:
    """Handle game initialization and the main game loop."""

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Maze Robot Simulation")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.maze = Maze(WIDTH, HEIGHT, CELL_SIZE)

        self.robot = Robot(self.maze, (CELL_SIZE * 1.5, CELL_SIZE * 1.5))
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False

    def run(self):
        """Run the main game loop."""
        running = True
        counter = 0
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            # Get the list of keys pressed
            keys = pygame.key.get_pressed()

            # Handle the controls
            vr, vl = self.handle_controls(keys)

            # Move the robot
            if vr != 0 or vl != 0:

                # move the robot with the diff drive model
                self.robot.move_with_diff_drive(vl, vr)

                if counter % self.robot.kalman_call_interval == 0:
                    # run the kalman filter
                    self.robot.run_kalman_filter(vl, vr)

            # Create the speed text
            speed_text = FONT.render(f'wheel power: {vl} | {vr}', True, WHITE)

            # reset the wheel power, to avoid continuous movement
            vr, vl = 0, 0

            # draw the maze, robot and speed cltext
            self.screen.fill(WHITE)
            self.maze.draw(self.screen)
            self.robot.draw_landmark_raycast(self.screen)
            self.robot.draw_path(self.screen)
            self.robot.update_sensors()
            self.robot.draw(self.screen)
            self.screen.blit(speed_text, (10, 10))

            pygame.display.flip()
            self.clock.tick(60)
            counter += 1

        pygame.quit()
    def handle_controls(self, keys):
        """Handle the controls for the robot."""
        # set the wheel power to 0
        vr, vl = 0, 0

        # if w is pressed, move the robot forward by 1
        if keys[pygame.K_w]:
            vr, vl = 1, 1

        # if s is pressed, move the robot backward by 1
        elif keys[pygame.K_s]:
            vr, vl = -1, -1

        # if a is pressed, turn the robot left
        if keys[pygame.K_a]:
            vr += 0.5
            vl += -0.5

        # if d is pressed, turn the robot right
        if keys[pygame.K_d]:
            vr += -0.5
            vl += 0.5

        # invert the controls, pygame treats the y axis as inverted
        vl, vr = vr, vl

        return vr, vl
        
if __name__ == "__main__":
    game = MazeGame()
    game.run()
    game.robot.plot_error()
