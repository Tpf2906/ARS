"""This test module checks the forward_kin module"""
from forward_kin import wall_angle

#TODO:(jounaid) consider add more tests
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

#TODO: (Jounaid) test other functions in forward_kin.py
