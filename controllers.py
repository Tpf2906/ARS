"""module for handling the controls of the game though various methods."""
import os
import numpy as np
import pygame

from evolution.genome import Genome
from evolution.genome import BasicGenome
from maze_game import MazeGame

def human_controls(game: MazeGame):
    """control the game with the keyboard."""
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #pylint: disable=no-member
                running = False

        keys = pygame.key.get_pressed()
        vr_input, vl_input = game.handle_controls(keys)
        game.step(vr_input, vl_input)

    pygame.quit() #pylint: disable=no-member

def ai_run(game: MazeGame, genome: Genome= None, steps: int= 200):
    """control the game with the ai."""
    episode_step_data = []

    # Initialize the state
    state_dict = {
        "sensors": game.robot.sensors,
        "collided": False,
        "dust_ratio": 0,
        "position": game.robot.estimated_positions[-1]
    }

    state = _flatten_state_dict(state_dict)

    #make sure the genome is not None
    if genome is None:
        genome = BasicGenome(state.shape[0])

    # Run the game for the specified number of steps
    for _ in range(steps):

        # Get the inputs from the genome
        vr_input, vl_input = genome.take_action(state)

        # normalize the inputs to be between -1 and 1
        vr_input = max(min(vr_input, 1), -1)
        vl_input = max(min(vl_input, 1), -1)

        # Step the game
        data = game.step(vr_input, vl_input)

        # Save the data
        episode_step_data.append(data)

    return episode_step_data

def _flatten_state_dict(state_dict):
    """
    Flattens the given state dictionary into a 1D numpy array of floats.
    
    Parameters:
    state_dict (dict): A dictionary containing sensor data, collision status,
                       dust ratio, and position.

    Returns:
    numpy.ndarray: A 1D numpy array of floats.
    """
    # Convert each element to a numpy array
    sensors_array = np.array(state_dict['sensors'], dtype=float)
    collided_array = np.array([state_dict['collided']], dtype=float)  # Convert bool to float
    dust_ratio_array = np.array([state_dict['dust_ratio']], dtype=float)
    position_array = np.array(state_dict['position'], dtype=float)

    # Concatenate all arrays into a single 1D array
    flattened_array = np.concatenate([sensors_array,
                                      collided_array,
                                      dust_ratio_array,
                                      position_array])

    return flattened_array

if __name__ == "__main__":
    # load the first .npy file in the genomes folder if it exists
    try:
        # check for file ending in .npy eplicitly
        genome_file = [file for file in os.listdir("genomes") if file.endswith(".npy")][0]

        # load the genome as dictionary
        genome_dict = np.load("genomes/" + genome_file, allow_pickle=True).item()

        # create the genome
        input_genome = BasicGenome(genome_dict=genome_dict)

    except FileNotFoundError:
        input_genome = None #pylint: disable=invalid-name

    test_game = MazeGame()
    ai_run(test_game, input_genome)
