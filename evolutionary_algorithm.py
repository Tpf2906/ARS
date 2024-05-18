# evolutionary_algorithm.py
import numpy as np
from ann import ANNController

class EvolutionaryAlgorithm:
    def __init__(self, population_size, input_size, hidden_size, output_size, mutation_rate=0.01, crossover_rate=0.7):
        self.population_size = population_size
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.population = [ANNController(input_size, hidden_size, output_size) for _ in range(population_size)]
    
    def evolve(self, fitness_scores):
        best_individuals = self.select_best_individuals(fitness_scores)
        new_population = self.create_new_population(best_individuals)
        self.population = new_population
        return max(fitness_scores)
    
    def select_best_individuals(self, fitness_scores):
        sorted_indices = np.argsort(fitness_scores)[::-1]
        return [self.population[i] for i in sorted_indices[:self.population_size // 2]]
    
    def create_new_population(self, best_individuals):
        new_population = best_individuals[:]
        while len(new_population) < self.population_size:
            parent1, parent2 = np.random.choice(best_individuals, 2, replace=False)
            child1, child2 = self.crossover(parent1, parent2)
            new_population.extend([self.mutate(child1), self.mutate(child2)])
        return new_population
    
    def crossover(self, parent1, parent2):
        child1 = ANNController(self.input_size, self.hidden_size, self.output_size)
        child2 = ANNController(self.input_size, self.hidden_size, self.output_size)
        if np.random.rand() < self.crossover_rate:
            weights1, weights2 = parent1.get_weights(), parent2.get_weights()
            crossover_point = np.random.randint(0, len(weights1))
            new_weights1 = np.concatenate((weights1[:crossover_point], weights2[crossover_point:]))
            new_weights2 = np.concatenate((weights2[:crossover_point], weights1[crossover_point:]))
            child1.set_weights(new_weights1)
            child2.set_weights(new_weights2)
        else:
            child1.set_weights(parent1.get_weights())
            child2.set_weights(parent2.get_weights())
        return child1, child2
    
    def mutate(self, individual):
        weights = individual.get_weights()
        for i in range(len(weights)):
            if np.random.rand() < self.mutation_rate:
                weights[i] += np.random.randn() * 0.1
        individual.set_weights(weights)
        return individual
