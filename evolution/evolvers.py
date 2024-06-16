"""module containing different evolver classes"""

from abc import ABC, abstractmethod
from random import uniform
from typing import List

from evolution.evaluators import Simple
from evolution.genome import Genome
from config.evolver_config import MUTATION_CHANCE

class Evolver(ABC):
    """an abstract class for all the different evolver classes"""
    def __init__(self, population_size, genome_class: callable, experiment_name=None):
        self.population_size = population_size
        self.genome_class: Genome = genome_class()
        self.best_genome = None
        self.evaluator = Simple()
        self.generations = 0

        # set experiment name
        if experiment_name is None:
            self.experiment_name = ''.join([chr(int(uniform(65, 90))) for _ in range(4)])
        else:
            self.experiment_name = experiment_name

        # Initialize the population
        self.population : List[Genome]= [genome_class() for _ in range(population_size)]

    @abstractmethod
    def evolve(self, number_of_generations):
        """evolve the population based on the episode step data"""

class Genitor(Evolver):
    """a class for the GENITOR algorithm"""
    def evolve(self, number_of_generations, mutation_chance=MUTATION_CHANCE):
        """run the GENITOR algorithm for the specified number of generations.
        Algorithm:
        1. Evaluate and rank the population
        2. Select the best two genomes
        3a. Crossover the best two genomes, creating one offspring
        3b. Mutate the offspring
        4. evaluate the offspring
        5. Replace the worst genome with the offspring
        
        Args:
            number_of_generations (int): the number of generations to run the algorithm for
        """

        for i in range(number_of_generations):
            # generate a new map set per generation
            self.evaluator.generate_map_set()

            # 1. Evaluate and rank the population
            for j, genome in enumerate(self.population):

                # Evaluate the genome
                self.evaluator.calculate_fitness(genome)
                print(f"Generation: {self.generations}, Cycle: {i}/{number_of_generations}, Genome: {j}, Fitness: {genome.fitness}") #pylint: disable=line-too-long

            # rank the population
            self.population.sort(reverse=True)

            # 2. Select the best two genomes
            best_genome = self.population[0]
            second_best_genome = self.population[1]

            # 3a. Crossover the best two genomes, creating one offspring
            offspring : Genome = self.genome_class.crossover(best_genome, second_best_genome)

            # 3b. Mutate the offspring at radom
            if mutation_chance > uniform(0,1):
                offspring.mutate()

            # 4. evaluate the offspring
            self.evaluator.calculate_fitness(offspring)

            # 5. Replace the worst genome with the offspring
            self.population.append(offspring)
            self.population.sort(reverse=True)
            self.population.pop()

            # update the best genome
            self.best_genome = self.population[0]
            self.best_genome.save_genome(f"best_genome_{self.experiment_name}_{self.generations}")

            # increment the generation
            self.generations += 1
            print()
