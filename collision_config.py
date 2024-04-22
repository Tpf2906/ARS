"""because of pixelswe need to define the angle a collison came from.
   these arethe corrrsponding x,t bits for each direction of collison
   these need to be updated every time the ROBOT_RADIUS is changed"""

from collison_calibration import run_calibration

# update these values when ROBOT_RADIUS is changed
NORTH = (10,0)
SOUTH = (10,25)
EAST = (25,10)
WEST = (0,10)

if __name__ == '__main__':
    run_calibration()
