"""this module tests the dust class"""
from dust import Dust
from config.maze_config import CELL_SIZE

def test_set_dust():
    """test the set dust method"""
    grid = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
    dust = Dust(grid)
    dust.set_dust()
    assert dust.intitial_dust_amount == 1
    assert dust.remaining_dust_amount == 1

def test_set_dust_on_landmark():
    """test the set dust method on a landmark"""
    grid = [[1, 1, 1], [1, 2, 1], [1, 1, 1]]
    dust = Dust(grid)
    dust.set_dust()
    assert dust.intitial_dust_amount == 1
    assert dust.remaining_dust_amount == 1

def test_clean_dust_round_pos():
    """test the clean dust method with a round position"""
    grid = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
    dust = Dust(grid)
    dust.set_dust()
    dust.clean_dust(CELL_SIZE, CELL_SIZE)
    assert dust.clean_ratio == 1

def test_clean_dust_round_pos_no_clean():
    """test the clean dust method with no dust to clean at a round position"""
    grid = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
    dust = Dust(grid)
    dust.set_dust()
    dust.clean_dust(0, 0)
    assert dust.clean_ratio == 0

def test_clean_dust_non_round_pos():
    """test the clean dust method with a non-round position"""
    grid = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
    dust = Dust(grid)
    dust.set_dust()
    dust.clean_dust(CELL_SIZE * 1.5, CELL_SIZE * 1.5)
    assert dust.clean_ratio == 1

def test_clean_dust_non_round_pos_no_clean():
    """test the clean dust method with no dust to clean at a non-round position"""
    grid = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
    dust = Dust(grid)
    dust.set_dust()
    dust.clean_dust(CELL_SIZE * 0.5, CELL_SIZE * 0.5)
    assert dust.clean_ratio == 0

def test_clean_dust_on_landmark():
    """test the clean dust method on a landmark"""
    grid = [[1, 1, 1], [1, 2, 1], [1, 1, 1]]
    dust = Dust(grid)
    dust.set_dust()
    dust.clean_dust(CELL_SIZE * 1.5, CELL_SIZE * 1.5)
    assert dust.clean_ratio == 1
    assert dust.remaining_dust_amount == 0
