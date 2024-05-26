# ARS Evolutionary Algorithm 3rd Assignment

## Overview
This project implements an evolutionary algorithm to optimize artificial neural network (ANN) configurations for robotic navigation in a maze environment. It includes modules for simulating a maze, robot dynamics, sensor inputs, and evolutionary strategies for training neural network controllers.

## Project Structure
- `test_game.py`: Main script to set up and compare different ANN configurations in the same maze environment.
- `ann.py`: Contains the implementation of the ANN controller used to control the robot.
- `evolutionary_algorithm.py`: Implements the evolutionary algorithm to evolve populations of ANN controllers.
- `fitness.py`: Defines the fitness function used to evaluate the performance of each individual in the population.
- `maze.py`: Module to generate and manage the maze environment in which the robot navigates.
- `robot.py`: Defines the Robot class that interacts with the maze and processes sensory inputs using the ANN controller.
- `forward_kin.py`: Contains the kinematics functions for the robot, including motion simulation with collision handling.
- `collision_config.py` and `collision_calibration.py`: Manage collision detection settings and calibration for the robot within the maze.
- `kalman_filter.py`: Implements the Kalman filter used for sensor fusion and state estimation of the robot. (Not needed for this 3rd assignment.)

## Dependencies
- Python 3.7+
- Pygame
- NumPy
- Matplotlib
- pygame_gui

## Installation
1. Ensure Python 3.7 or newer is installed.
2. Install the required packages using pip:
   ```bash
   pip install numpy pygame matplotlib pygame_gui

## Usage
To run the simulations and train the ANN using the evolutionary algorithm:
`python test_game.py`

This script initializes the game environment, loads the maze, and starts the simulation where different neural network configurations are tested.

## Configuration
Modify the ANN configurations, evolutionary parameters, or the maze setup in the respective `.py` files to experiment with different settings and observe the behavior of the robot in the maze environment.