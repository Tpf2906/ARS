"""Run the evolution experiment."""
import argparse

from config.robot_config import SENSOR_MAX_DISTANCE, SENSOR_NOISE_DEFAULT
from config.maze_config import MAP_NAME
from evolution.evolvers import Genitor
from evolution.genome import BasicGenome

def parse_arguments():
    """Parse command line arguments."""
    #pylint: disable=line-too-long
    parser = argparse.ArgumentParser(description="Simulation Parameters")
    parser.add_argument("--experiment_name", type=str,required=True, help="Name of the experiment")
    parser.add_argument("--sensor_noise", type=float, default=SENSOR_NOISE_DEFAULT, help="Noise level for the sensors")
    parser.add_argument("--max_sensor_length", type=int, default=SENSOR_MAX_DISTANCE, help="Maximum length of the sensor")
    parser.add_argument("--mutation_chance", type=float, default=0.1, help="Probability of mutation")
    parser.add_argument("--population_size", type=int, default=50, help="Size of the population")
    parser.add_argument("--generations", type=int, default=100, help="Number of generations")
    #pylint: enable=line-too-long

    return parser.parse_args()

def run_experiment(population_size, generations, experiment_name, mutation_chance):
    """Run the evolution experiment."""
    evolver = Genitor(population_size=population_size,
                      genome_class=BasicGenome,
                      experiment_name=experiment_name)
    evolver.evolve(number_of_generations=generations, mutation_chance=mutation_chance)

def main():
    """Main function to run the experiment."""
    args = parse_arguments()
    run_experiment(args.population_size, args.generations, args.experiment_name, args.mutation_chance) #pylint: disable=line-too-long

if __name__ == "__main__":
    main()
