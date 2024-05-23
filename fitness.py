'''
This file contains the fitness function to determine the fitness of the robot with the given 
controller to make it move and return the explored area
'''
import numpy as np

def fitness(robot, ann_controller, steps=500):
    '''
    determine the fitness of the robot with the given controller to make it move and return the explored area
    '''
    robot.reset()
    for _ in range(steps):
        sensors = robot.sensors
        inputs = np.array(sensors).flatten()
        vl, vr = ann_controller.forward(inputs)
        robot.move_with_diff_drive(vl, vr)
        robot.update_sensors()
    return robot.calculate_explored_area()