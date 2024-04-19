"""Forward kinematics for the robot"""
import numpy as np
from robot_config import ROBOT_RADIUS

L = ROBOT_RADIUS # distance between wheels

#TODO: (Jounaid) consider passing the Robot rather thaan the state
def motion_without_collison(state, d_t):
    """state change not accounting for collisions"""

    # Unpack state
    x, y = state[0], state[1]
    theta = state[2]
    v_l, v_r = state[3], state[4]

    # intermediate variables
    omega = (v_r - v_l) / L

    # calculate new state
    # handle special case of straight line
    if v_l == v_r:
        x += v_l * np.cos(theta) * d_t
        y += v_l * np.sin(theta) * d_t
        # theta = theta

    # handle opposite directions
    elif v_l == -v_r:
        x += 0
        y += 0
        theta += omega * d_t

    # handle general case
    else:
        # intermidiate variables
        r = L / 2 * (v_l + v_r) / (v_r - v_l)
        icc = (x - r * np.sin(theta), y + r * np.cos(theta))

        # calculate new x, y, and theta
        x = (x-icc[0]) * np.cos(omega * d_t) - (y-icc[1]) * np.sin(omega * d_t) + icc[0]
        y= (x-icc[0]) * np.sin(omega * d_t) + (y-icc[1]) * np.cos(omega * d_t) + icc[1]
        theta = theta + omega * d_t

    # theta wrap around
    theta = theta % (2 * np.pi)
    # new x, y, and theta
    return np.array([x, y, theta])

def motion_with_collision(state, d_t):
    """state change accounting for collisions"""
    raise NotImplementedError

#TODO:(@Jounaid) Robot_racasting is useful outside of the robot class, consider moving it to a utility file pylint: disable=line-too-long
def wall_angle(sensors):
    """Calculate the angle of the  wall, relative to the shortest sensor reading.
       to simplify the syntax we will work directly with the maths:

       side_a is the shortest sensor reading
       side_b is the shortest senor reading adjacent to side_b
       angle_c is the angle between side_a and side_b

       angle_b is the anngle of the wall(side_c) relative to side_a
       angle_b is therefore the angle of the wall relative to the shortest sensor reading
       """

    # find the shortest sensor reading
    side_a = min(sensors)
    index_a = sensors.index(side_a)

    # get side_b candidates, the adjacent sensors
    index_b_candidates = [index_a - 1 % len(sensors), index_a + 1 % len(sensors)]
    side_b_candidates = [sensors[index_b_candidates[0]], sensors[index_b_candidates[1]]]

    # find the shortest side_b and its index
    side_b = min(side_b_candidates)
    index_b = sensors.index(side_b)

    # calculate angle_c
    angle_c = 2 * np.pi / len(sensors)

    # calculate side_c
    side_c = np.sqrt(side_a**2 + side_b**2 - 2 * side_a * side_b * np.cos(angle_c))

    # calculate angle_b, using the sine rule
    angle_b = np.arcsin(side_b * np.sin(angle_c) / side_c)

    # convert radians to degrees
    angle_b = np.degrees(angle_b)

    # return index of the two sensors and the angle of the wall
    return index_a, index_b, angle_b
