import numpy as np

# TODO: fix where we get l from
l = 10 # distance between wheels

def raw_state_change(state, d_t):
    """state change not accounting for collisions"""

    # Unpack state
    x, y = state[0], state[1]
    theta = state[2]
    v_l, v_r = state[3], state[4]    

    # intermediate variables
    v  = 0.5 * (v_l + v_r)
    r = 0.5 * (v_l + v_r) / (v_r - v_l)
    omega = (v_r - v_l) / l
    icc = (x - r * np.sin(theta), y + r * np.cos(theta))

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
        x = np.cos(theta * d_t) * (x - icc[0]) - np.sin(theta * d_t) * (y - icc[1]) + icc[0]
        y = np.sin(theta * d_t) * (x - icc[0]) + np.cos(theta * d_t) * (y - icc[1]) + icc[1]
        theta += omega * d_t

    # new x, y, and theta
    return np.array([x, y, theta]) 