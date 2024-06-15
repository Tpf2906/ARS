"""a module containing all the different controllers as different genome classes"""\

from abc import ABC, abstractmethod

import numpy as np

class Genome(ABC):
    """an abstract class for all the different genome classes"""
    def __init__(self, input_size=None, genome_dict=None):
        if input_size is not None:
            # Initialize weights and biases
            self.weights = np.random.randn(input_size, 2)
            self.biases = np.random.randn(2)
            self.fitness = None
        else:
            # Load the genome from a dictionary
            self.weights = genome_dict["weights"]
            self.biases = genome_dict["biases"]
            self.fitness = genome_dict["fitness"]

    def take_action(self, state):
        """take an action based on the input X"""
        # Perform the forward pass
        output = np.dot(state, self.weights) + self.biases
        return output

    def save_genome(self, name):
        """save the genome to a dictionary"""
        # Save the genome to a dictionary
        genome_dict = {
            "weights": self.weights,
            "biases": self.biases,
            "fitness": self.fitness
        }

        # Save the dictionary to a .npy file
        location = "genomes/" + name + ".npy"
        np.save(location, genome_dict)

    def __lt__(self, other):
        return self.fitness < other.fitness

    @staticmethod
    @abstractmethod
    def crossover(first, second):
        """crossover the genome with another genome"""

    @abstractmethod
    def mutate(self):
        """mutate the genome"""

class BasicGenome(Genome):
    """genome is the weights and biases of a neural network.
       mutation are uniform around weights and biases respectively
       crossover is a switch bewteem subsets of weight-bias pairs"""

    @staticmethod
    def crossover(first, second):
        """crossover the genome with another genome"""
        # generate two random indexes as crossover points
        points = np.random.randint(0, first.weights.shape[0], 2)
        first_point, second_point = min(points), max(points)

        # create the offspring genome
        weight = np.concatenate((first.weights[:first_point], 
                                 second.weights[first_point:second_point], # crossover segment
                                 first.weights[second_point:]), axis=0)

        bias = np.concatenate((first.biases[:first_point],
                               second.biases[first_point:second_point], # crossover segment
                               first.biases[second_point:]), axis=0)

        # create genome_dict
        genome_dict = {
            "weights": weight,
            "biases": bias,
            "fitness": None
        }

        return BasicGenome(None, genome_dict)

    def mutate(self):
        """mutate the genome"""
        # random choice between weight and bias
        choice = np.random.choice([0, 1])

        # random index for mutation
        index = np.random.randint(0, self.weights.shape[0])

        # mutate the genome
        if choice == 0:
            self.weights[index] += np.random.uniform(-0.1, 0.1)
        else:
            self.biases[index] += np.random.uniform(-0.1, 0.1)
