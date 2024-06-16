"""Run the evolution experiment."""
import argparse

from config.robot_config import SENSOR_MAX_DISTANCE, SENSOR_NOISE_DEFAULT
from config.evolver_config import MUTATION_CHANCE

from evolution.evolvers import Genitor
from evolution.genome import BasicGenome

def parse_arguments():
    """Parse command line arguments."""
    #pylint: disable=line-too-long
    parser = argparse.ArgumentParser(description="Simulation Parameters")
    parser.add_argument("--sensor_noise", type=float, default=SENSOR_NOISE_DEFAULT, help="Noise level for the sensors")
    parser.add_argument("--max_sensor_length", type=int, default=SENSOR_MAX_DISTANCE, help="Maximum length of the sensor")
    parser.add_argument("--mutation_probability", type=float, default=MUTATION_CHANCE, help="Probability of mutation")
    parser.add_argument("--population_size", type=int, default=50, help="Size of the population")
    parser.add_argument("--generations", type=int, default=100, help="Number of generations")
    #pylint: enable=line-too-long

    return parser.parse_args()

def set_experiment_parameters(args):
    """Set parameters for the experiment based on parsed arguments."""
    global SENSOR_NOISE_DEFAULT, SENSOR_MAX_DISTANCE, MUTATION_CHANCE #pylint: disable=global-statement
    SENSOR_NOISE_DEFAULT = args.sensor_noise
    SENSOR_MAX_DISTANCE = args.max_sensor_length
    MUTATION_CHANCE = args.mutation_probability

def run_experiment(population_size, generations):
    """Run the evolution experiment."""
    evolver = Genitor(10, BasicGenome)
    evolver.evolve(population_size, generations)

def main():
    """Main function to run the experiment."""
    args = parse_arguments()
    set_experiment_parameters(args)
    run_experiment(args.population_size, args.generations)

if __name__ == "__main__":
    main()
