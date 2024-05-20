import numpy as np

#makes robot move and returns the explored area

def fitness(robot, ann_controller, steps=500):
    robot.reset()
    for _ in range(steps):
        sensors = robot.sensors
        position = (robot.x, robot.y)
        angle = robot.angle
        inputs = np.concatenate((sensors, [position[0], position[1], angle]))
        vl, vr = ann_controller.forward(inputs)
        robot.move_with_diff_drive(vl, vr)
        robot.update_sensors()
    return robot.calculate_explored_area()