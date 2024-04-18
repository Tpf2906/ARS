""" main.py used to run the game """
# disabling pylint no-member error for pygame
# pylint: disable=no-member
import pygame 
from maze import Maze, WIDTH, HEIGHT, CELL_SIZE, NUM_ROOMS, ROOM_SIZE, BLACK
from robot import Robot


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
            if not (self.moving_up or self.moving_down or self.moving_left or self.moving_right):
                self.robot.speed = 0

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
