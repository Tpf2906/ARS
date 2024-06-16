"""module for playing a genome on corresponding maps"""

import argparse
import os
import numpy as np

import matplotlib.pyplot as plt

from controllers import ai_run
from evolution.genome import BasicGenome
from maze_game import MazeGame

# get experiment name
parser = argparse.ArgumentParser()
parser.add_argument("experiment_name", help="Name of the experiment")
args = parser.parse_args()

# get all map files containing the experiment_name in their name and ending with .npy
files = [f for f in os.listdir("maps") if args.experiment_name in f and f.endswith(".npy")]

# print the file names
for f in files:
    print(f)

# load all maps
maps = [np.load(f"maps/{f}", allow_pickle=True) for f in files]

# get all genome files containing the experiment_name in their name and ending with .npy
files = [f for f in os.listdir("genomes") if args.experiment_name in f and f.endswith(".npy")]



# load all genomes
genomes = [np.load(f"genomes/{f}", allow_pickle=True) for f in files]

# select 4 inexes linearly spaced including the first and last genome
indexes = np.round(np.linspace(0, len(genomes)-1, 4)).astype(int)

# select the genomes and maps
genomes = [genomes[i] for i in indexes]

# set step length for each genome (50 + genome index * 10)
step_lengths = [50 + 10 * i for i in indexes]

finesses = []

# play the genomes on the all maps
for genome, step_length in zip(genomes, step_lengths):
    genome_dict = dict(enumerate(genome.flatten()))[0]
    finesses.append(genome_dict["fitness"])
    genome = BasicGenome(genome_dict=genome_dict)
    for map_data in maps:
        game = MazeGame(grid_map=map_data)
        ai_run(game, genome, step_length)

# plot the finesses, as scatter plot (index, fitness)
plt.scatter(indexes, finesses)
plt.xlabel("Genome Index")
plt.ylabel("Fitness")
plt.title(f"Best Fitness of the genomes ({args.experiment_name})")
plt.show()
