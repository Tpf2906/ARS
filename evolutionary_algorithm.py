'''
this file contains the implementation of the evolutionary algorithm
'''

import numpy as np
from ann import ANNController
from fitness import fitness


class EvolutionaryAlgorithm:
    '''
    evolutionary algorithm to evolve the population of controllers
    '''
    def __init__(self, population_size, input_size, hidden_size, output_size,robot, mutation_rate=0.01, crossover_rate=0.7):
        '''
        initialize the evolutionary algorithm with the given parameters
        '''
        self.population_size = population_size
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.robot = robot
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.population = [ANNController(input_size, hidden_size, output_size) for _ in range(population_size)]
    

    def evolve(self):
        '''
        evolve the population and evaluate the fitness of the individuals and replace the 
        least fit individual with the child and continue the process until the time limit is reached
        '''
        fitness_scores = self.evaluate_fitness()
        # Sort the population by fitness
        self.rank_population(fitness_scores)
        while True:
            # Select two parents based on fitness
            parent1, parent2 = self.select_parents(fitness_scores)
            # Create a child by crossover and mutation
            child = self.create_child(parent1, parent2)
            print("Child created")
            child_fitness = fitness(self.robot, child)
            # Insert the child into the population if it is fitter than the least fit individual
            if self.insert_child_if_fitter(child, child_fitness, fitness_scores):
                fitness_scores = self.evaluate_fitness()  # Re-evaluate fitness scores after insertion
            else:
                break
            
 
    def evaluate_fitness(self):
        '''
        evaluate the fitness of each individual in the population
        '''
        return np.array([fitness(self.robot,individual) for individual in self.population])
    

    def rank_population(self, fitness_scores):
        '''
        sort the population by fitness
        '''
        sorted_indices = np.argsort(fitness_scores)[::-1]
        self.population = [self.population[i] for i in sorted_indices]

    
    def select_parents(self, fitness_scores):
        '''
        select two parents based on fitness
        '''
        probabilities = fitness_scores / fitness_scores.sum()  
        parents_indices = np.random.choice(len(self.population), 2, p=probabilities) #bigger fitness, bigger probability
        return self.population[parents_indices[0]], self.population[parents_indices[1]]
    
    
    def create_child(self, parent1, parent2):
        '''
        create a child by crossover and mutation
        '''
        child = ANNController(self.input_size, self.hidden_size, self.output_size)
        # check if crossover happens
        if np.random.rand() < self.crossover_rate:
            weights1, weights2 = parent1.get_weights(), parent2.get_weights()
            crossover_point = np.random.randint(0, len(weights1))
            new_weights = np.concatenate((weights1[:crossover_point], weights2[crossover_point:]))
            child.set_weights(new_weights)
        else:
            child.set_weights(parent1.get_weights())
        return self.mutate(child)
    
    

    def mutate(self, individual):
        '''
        mutate the weights of the individual
        '''
        weights = individual.get_weights()
        for i in range(len(weights)):
            if np.random.rand() < self.mutation_rate:
                weights[i] += np.random.randn() * 0.1
        individual.set_weights(weights)
        return individual
    
    
    def insert_child_if_fitter(self, child, child_fitness, fitness_scores):
        '''
        insert the child into the population if it is fitter than the least fit individual
        '''
        min_fitness_index = np.argmin(fitness_scores)
        if child_fitness > fitness_scores[min_fitness_index]:
            self.population[min_fitness_index] = child # Replace the individual with the lowest fitness
            return True
        return False
