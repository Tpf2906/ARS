# TODO: (Tiago) please do a pylint check and fix the issues in the code.
# remove the next line to see the pylint issues
# pylint: disable=invalid-name
# pylint: disable=missing-class-docstring
import unittest
import numpy as np
from kalman_filter import KalmanFilter

class TestKalmanFilter(unittest.TestCase):
    def setUp(self):
        self.A = np.eye(3)
        self.B = np.eye(3)
        self.Q = np.eye(3) * 0.01  # for the state vector (3x3)
        self.R = np.eye(4) * 0.02  # for 4 measurements
        self.initial_state = np.array([0, 0, 0])
        self.initial_P = np.eye(3) * 0.1  # state uncertainty
        self.kf = KalmanFilter(self.A, self.B, np.eye(3), self.Q,
                               self.R, self.initial_state, self.initial_P)
        self.landmarks = [(10, 10), (1, 1)]


    def test_predict_and_correct(self):
        """
        Test the predict and correct methods of the Kalman Filter
        """
        # control vector simulates the robot movement
        control_vector = np.array([1, 0.1, 0.05])  # move forward by 1, slight turn

        # prediction step
        self.kf.predict(control_vector)

        # simulate measurement acquisition
        measurements = self.kf.h(self.kf.state_estimate, self.landmarks)

        # correction step
        self.kf.correct(measurements, self.landmarks)

        estimated_state = self.kf.state_estimate()
        print("Estimated state:", estimated_state)
        self.assertTrue(np.allclose(estimated_state, np.array([1, 0.1, 0.05]), atol=1e-2))

    def test_initial_state(self):
        """
        Test the initial state setting
        """
        self.assertEqual(self.kf.state_estimate.tolist(), [0, 0, 0])

if __name__ == '__main__':
    unittest.main()
