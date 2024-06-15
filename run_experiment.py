"""module to run the experiment"""
# create the evolver
from evolution.evolvers import Genitor
from evolution.genome import BasicGenome

evolver = Genitor(10, BasicGenome)

# evolve the population
evolver.evolve(10)
