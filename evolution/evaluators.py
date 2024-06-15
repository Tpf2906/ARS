"""module contaaining different fitness functions"""
from abc import ABC, abstractmethod

from evolution.genome import Genome
from controllers import ai_run
from maze_game import MazeGame
from maze import Maze

class Evaluator(ABC):
    """an abstract class for all the different fitness functions"""
    def __init__(self, number_of_maps=5):
        self.grid = []
        for _ in range(number_of_maps):
            self.grid.append(Maze().grid)

    def calculate_fitness(self, genome: Genome):
        """ fitness function that takes the percentage of dust cleaned minus the collisions"""
        # reset the fitness
        genome.fitness = None
        scores = []
        for grid in self.grid:

            # run the genome on the map
            episode_step_data = ai_run(MazeGame(grid_map=grid), genome)
            # calculate the fitness
            score = self._calculate_score(episode_step_data)

            # append the score to the list of scores
            scores.append(score)

        # calculate the average score
        genome.fitness = sum(scores) / len(scores)

    @abstractmethod
    def _calculate_score(self, episode_step_data):
        """calculate the score based on the episode step data""" 

class Simple(Evaluator):
    """calculate the score as dust cleaned minus the collisions per step"""
    def _calculate_score(self, episode_step_data):
        """calculate the score as dust cleaned minus the collisions per step"""

        # number of True in the collisions list
        collisions = sum([1 for data in episode_step_data if data["collided"]])

        # calculate the score
        score = episode_step_data[-1]["dust_ratio"] - collisions / len(episode_step_data)

        return score