"""because of pixelswe need to define the angle a collison came from.
   these arethe corrrsponding x,t bits for each direction of collison
   these need to be updated every time the ROBOT_RADIUS is changed"""

import numpy as np
from collison_calibration import run_calibration

# update these values when ROBOT_RADIUS is changed
NORTH = (10,0)
SOUTH = (10,25)
EAST = (25,10)
WEST = (0,10)

max_x = max(NORTH[0], SOUTH[0], EAST[0], WEST[0])
max_y = max(NORTH[1], SOUTH[1], EAST[1], WEST[1])

CENTER = np.array((max_x // 2, max_y // 2))

if __name__ == '__main__':
    run_calibration()
