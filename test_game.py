'''
This file is used to compare different ANN configurations in the same maze environment.
'''

import os
import multiprocessing
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pygame
import pygame_gui
from maze import Maze
from config.maze_config import WIDTH, HEIGHT, CELL_SIZE, WHITE
from robot import Robot
from evolutionary_algorithm import EvolutionaryAlgorithm


class TestGame:
    """
    Compare different ANN configurations in the same maze environment.
    """
    def __init__(self, population_file=None, output_file=None, grid=None, rect_list=None, landmarks=None):
        '''
        initialize the game with the given population file and output file name
        '''
        pygame.init()
        pygame.display.set_caption("Maze Robot Simulation")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.maze = Maze(WIDTH, HEIGHT, CELL_SIZE, grid=grid, rect_list=rect_list, landmarks=landmarks)
        self.robot = Robot(self.maze, (CELL_SIZE * 1.5, CELL_SIZE * 1.5))
        self.manager = pygame_gui.UIManager((WIDTH, HEIGHT))
        self.evo_algorithm = EvolutionaryAlgorithm(population_size=20, input_size=12, hidden_size=10, output_size=2, robot=self.robot)
        self.population_file = population_file
        self.output_file = output_file
        if population_file:
            self.load_robot_population(population_file)


    def run(self):
        """
        Run the main game loop, ending after 30 seconds.
        """
        running = True
        start_time = pygame.time.get_ticks()
        
        while running:
            current_time = pygame.time.get_ticks()
            if (current_time - start_time) >= 30000:
                running = False

            time_delta = self.clock.tick(60)/1000.0
            self.manager.update(time_delta)
            sensors = self.robot.sensors
            inputs = np.array(sensors).flatten()

            vl, vr = self.evo_algorithm.population[0].forward(inputs)

            if vr != 0 or vl != 0:
                self.robot.move_with_diff_drive(vl, vr)

            self.screen.fill(WHITE)
            self.maze.draw(self.screen)
            self.robot.draw_landmark_raycast(self.screen)
            self.robot.draw_path(self.screen)
            self.robot.update_sensors()
            self.robot.draw(self.screen)
            self.manager.draw_ui(self.screen)

            pygame.display.flip()

        if self.output_file:
            pygame.image.save(self.screen, self.output_file)

        pygame.quit()
        return self.robot.calculate_explored_area()


    def load_robot_population(self, population_file):
        '''
        load the weights of the robot from a file
        '''
        if os.path.exists(population_file):
            weights = np.load(population_file)
            self.evo_algorithm.population[0].set_weights(weights)
        else:
            print(f"Error: File {population_file} does not exist.")


def run_experiment(weight_file, grid, rect_list, landmarks):
    '''
    run the experiment with the given weight file and return the explored area
    '''
    output_file = f'final_{weight_file.replace(".npy", "")}.png'
    game = TestGame(population_file=weight_file, output_file=output_file, grid=grid, rect_list=rect_list, landmarks=landmarks)
    return game.run()


def main():
    '''
    run the main function to compare different ANN configurations in the same maze environment
    '''
    maze = Maze(WIDTH, HEIGHT, CELL_SIZE)
    grid, rect_list, landmarks = maze.grid, maze.rect_list, maze.landmarks

    weight_files = [
        '5thgen10pop.npy',
        '5thgen20pop.npy',
        '20thgen10pop.npy',
        '20thgen20pop.npy',
        'highmutation.npy',
        'highsensornoise.npy'
    ]
    
    # use multiprocessing to run experiments in parallel
    pool = multiprocessing.Pool(processes=6)
    results = pool.starmap(run_experiment, [(wf, grid, rect_list, landmarks) for wf in weight_files])

    # plotting results for all 6 experiments
    rows = 2
    cols = 3
    fig, axs = plt.subplots(rows, cols, figsize=(15, 10))
    
    # check if axs is a single-dimensional array, if not, flatten it
    axs = axs.flatten() if rows > 1 else [axs]

    for i, weight_file in enumerate(weight_files):
        img_path = f'final_{weight_file.replace(".npy", ".png")}'
        img = mpimg.imread(img_path)
        axs[i].imshow(img)
        axs[i].set_title(weight_file.replace(".npy", ""))
        axs[i].axis('off')

    plt.tight_layout()
    plt.savefig('final_maze_comparison.png')
    plt.show()
    
    # plotting results for explored area
    fig, ax = plt.subplots(figsize=(12, 9))
    ax.bar(weight_files, results, color='blue')
    ax.set_title('Explored Area by Different ANNs')
    ax.set_xlabel('Weight File')
    ax.set_ylabel('Explored Area')
    plt.xticks(rotation=20)
    plt.savefig('explored_area_comparison.png')
    plt.show()
        
if __name__ == "__main__":
    main()
