"""This test module checks the forward_kin module"""
from forward_kin import wall_angle, motion_without_collison

class TestWallAngle:
    """Test the wall angle function"""
    def test_shortes_sensor(self):
        """checks that the wall angle function returns the correct smallest sensor
        and its smallest adjacent sensor"""

        result = wall_angle([1, 2, 3, 4])
        assert result[0] == 0 and result[1] == 1

        result = wall_angle([1, 0, 1, 4])
        assert result[0] == 1 and (result[1] == 0 or result[1] == 2)

    def test_wall_angle(self):
        """checks that the wall angle function returns the correct wall angle
        and the correct sensor indeces"""
        result = wall_angle([100, 100, 2, 4, 5, 100])
        assert result == (2, 3, 90.0)

class TestMotionWithoutCollision:
    """Test the motion without collision function"""
    def test_vl_equal_vr(self):
        """checks that the robot moves in a straight line"""

        # test moving straight forward
        x, y, theta = motion_without_collison([0, 0, 0, 1,1,], 1)
        assert x == 1 and y == 0 and theta == 0

        # test moving straight backward
        x, y, theta = motion_without_collison([0, 0, 0, -1,-1,], 1)
        assert x == -1 and y == 0 and theta == 0

    def test_vl_equal_minus_vr(self):
        """checks that the robot rotates in place"""

        # test rotating clockwise
        x, y, theta = motion_without_collison([0, 0, 0, 1,-1], 1)
        assert x == 0 and y == 0 and theta != 0

        # test rotating counter clockwise
        x, y, theta = motion_without_collison([0, 0, 0, -1,1], 1)
        assert x == 0 and y == 0 and theta != 0

    def test_vl_not_equal_vr(self):
        """checks that the robot moves in a curve"""
        #check left wheel spin with dead right wheel
        x, y, theta = motion_without_collison([0, 0, 0, 1, 0], 1)
        assert x != 0.0 and y != 0.0 and theta != 0.0

        #check right wheel spin with dead left wheel
        x, y, theta = motion_without_collison([0, 0, 0, 0, 1], 1)
        assert x != 0.0 and y != 0.0 and theta != 0.0

        #check both wheels spinning
        x, y, theta = motion_without_collison([0, 0, 0, 1, 2], 1)
        assert x != 0.0 and y != 0.0 and theta != 0.0
