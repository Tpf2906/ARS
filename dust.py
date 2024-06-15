"""mudule holding methods to calculae the dust method"""

from config.maze_config import CELL_SIZE

class Dust:
    """This class contains the dust information for the maze game."""
    def __init__(self, grid):
        self.grid = grid
        self.dust = [[0 for x in range(len(grid[0]))] for y in range(len(grid))]
        self.intitial_dust_amount = 0
        self.remaining_dust_amount = 0
        self.clean_ratio = 0

    def set_dust(self):
        "set the dust on the grids where the grid is a landmark or floor tile (not a wall)"

        # set the dust on the grid
        for y, _ in enumerate(self.grid):
            for x, _ in enumerate(self.grid[0]):
                if self.grid[y][x] != 1:
                    self.dust[y][x] = 1
                    self.intitial_dust_amount += 1

        # update the remaining dust amount
        self.remaining_dust_amount = self.intitial_dust_amount

    def clean_dust(self, x, y):
        "clean the dust on the grid"
        # calculate the grid position
        x = int(x / CELL_SIZE)
        y = int(y / CELL_SIZE)

        # check if the grid has dust
        if self.dust[y][x] == 1:

            # clean the dust on the grid
            self.dust[y][x] = 0
            self.remaining_dust_amount -= 1

            # calculate the clean ratio
            cleaned_dust = self.intitial_dust_amount - self.remaining_dust_amount
            self.clean_ratio = cleaned_dust / self.intitial_dust_amount

        # return the ratio
        return self.clean_ratio
