""" main.py used to run the game """
# disabling pylint no-member error for pygame
# pylint: disable=no-member
import pygame
from maze import Maze
from maze_config import WIDTH, HEIGHT, CELL_SIZE, NUM_ROOMS, ROOM_SIZE, BLACK, WHITE, FONT
from robot import Robot


class MazeGame:
    """Handle game initialization and the main game loop."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.maze = Maze(WIDTH, HEIGHT, CELL_SIZE)

        #TODO: move to Maze class __init__
        self.maze.dfs(1, 1)
        self.maze.create_rooms(NUM_ROOMS, ROOM_SIZE)
        self.robot = Robot(self.maze, (CELL_SIZE * 1.5, CELL_SIZE * 1.5))  # Starting the robot in the first cell, pylint: disable=line-too-long
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False

    def run(self):
        """Run the main game loop."""
        running = True
        vr, vl = 0, 0
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            # Get the list of keys pressed
            keys = pygame.key.get_pressed()

            # update left wheel
            if keys[pygame.K_q]:
                vl = 1
            elif keys[pygame.K_a]:
                vl = -1
            else:
                vl = 0

            # update right wheel
            if keys[pygame.K_e]:
                vr = 1
            elif keys[pygame.K_d]:
                vr = -1
            else:
                vr = 0

            # Move the robot
            if vr != 0 or vl != 0:
                # add some spin to prevent dead whe
                if vr == 0 and vl != 0:
                    vr = vl * 0.7

                if vl == 0 and vr != 0:
                    vl = vr * 0.7

                self.robot.move_with_diff_drive(vl, vr)

            self.screen.fill(BLACK)
            self.maze.draw(self.screen)
            self.robot.update_sensors()
            self.robot.draw(self.screen)

            # Display the speed of the robot (0 or 2)
            speed_text = FONT.render(f'Speed: {self.robot.speed}', True, WHITE)
            self.screen.blit(speed_text, (10, 10))

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = MazeGame()
    game.run()
