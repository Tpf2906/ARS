import numpy as np
import pytest
from kalman_filter import KalmanFilter

@pytest.fixture
def kf():
    A = np.eye(3)
    B = np.eye(3)
    Q = np.eye(3) * 0.01  # for the state vector (3x3)
    R = np.eye(4) * 0.02  # for 4 measurements
    initial_state = np.array([0, 0, 0])
    initial_P = np.eye(3) * 0.1  # state uncertainty
    kalman_filter = KalmanFilter(A, B, np.eye(3), Q, R, initial_state, initial_P)
    landmarks = [(10, 10), (1, 1)]
    return kalman_filter, landmarks

def test_predict_and_correct(kf):
    kalman_filter, landmarks = kf
    # control vector simulates the robot movement
    control_vector = np.array([1, 0.1, 0.05])  # move forward by 1, slight turn

    # prediction step
    kalman_filter.predict(control_vector)

    # simulate measurement acquisition
    measurements = kalman_filter.h(kalman_filter.state_estimate, landmarks)

    # correction step
    kalman_filter.correct(measurements, landmarks)

    estimated_state = kalman_filter.state_estimate
    print("Estimated state:", estimated_state)
    assert np.allclose(estimated_state, np.array([1, 0.1, 0.05]), atol=1e-2), "Estimated state does not match expected" #pylint: disable=line-too-long

def test_initial_state(kf):
    kalman_filter, _ = kf
    assert kalman_filter.state_estimate.tolist() == [0, 0, 0], "Initial state is not as expected"
