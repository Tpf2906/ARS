"""config file for robot.py"""
from config import maze_config

ROBOT_RADIUS = maze_config.CELL_SIZE // 3
ROBOT_COLOR = (255, 0, 0)
SENSOR_COLOR = (255, 0, 0)
SENSOR_COLOR_LANDMARK = (0, 255, 0)
SENSOR_COLOR_FORWARD = (0, 0, 255)
TEXT_COLOR = (255,0, 255)
TEXT_COLOR_SPEED = (0, 0, 0)
NUM_SENSORS = 12
SENSOR_MAX_DISTANCE = maze_config.WIDTH
ROBOT_SPEED = 2
