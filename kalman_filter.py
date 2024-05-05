"""
kalman_filter.py: Class to calculate the Kalman filter.
"""

import numpy as np

class KalmanFilter:
    """
    Kalman Filter with initializations.
    """
    def __init__(self, state_transition_matrix, control_input_matrix, observation_matrix,
                 noise_covariance, noise_covariance_measurement, state_estimate, error_covariance):
        """
        Initialize the Kalman Filter
        :param state_transition_matrix: Transition matrix
        :param control_input_matrix: Control-input matrix
        :param observation_matrix: Observation matrix
        :param noise_covariance: Process noise covariance
        :param noise_covariance_measurement: Measurement noise covariance
        :param state_estimate: Initial state estimate
        :param error_covariance: Initial error covariance
        """
        self.state_transition_matrix = state_transition_matrix # A
        self.control_input_matrix = control_input_matrix  # B
        self.observation_matrix = observation_matrix  # C
        self.noise_covariance = noise_covariance  # Q
        self.noise_covariance_measurement = noise_covariance_measurement  # R
        self.state_estimate = state_estimate  # x
        self.error_covariance = error_covariance  # P


    def predict(self, control_vector):
        """
        Prediction step of the Kalman Filter
        :param control_vector: The control input
        """
        # State prediction
        self.state_estimate = np.dot(
            self.state_transition_matrix, self.state_estimate
            ) + np.dot(self.control_input_matrix, control_vector)
        # Covariance prediction
        self.error_covariance = np.dot(np.dot(
            self.state_transition_matrix, self.error_covariance
            ), self.state_transition_matrix.T) + self.noise_covariance


    def correct(self, measurement_vector, landmarks):
        """
        Correction step of the Kalman Filter
        :param measurement_vector: The measurement input
        """
        observation_matrix = self.jacobian_c(self.state_estimate, landmarks)

        # Kalman Gain calculation
        state = np.dot(observation_matrix, np.dot(
            self.error_covariance, observation_matrix.T)
                       ) + self.noise_covariance_measurement
        
        kalman_gain = np.dot(np.dot(
            self.error_covariance, observation_matrix.T
            ), np.linalg.inv(state))
        
        y = measurement_vector - self.h(self.state_estimate, landmarks)

        # State update
        self.state_estimate = self.state_estimate + np.dot(kalman_gain, y)

        # Covariance update
        identity_matrix = np.eye(self.state_transition_matrix.shape[0])
        self.error_covariance = np.dot((identity_matrix - np.dot(kalman_gain, observation_matrix)),
                                        self.error_covariance)


    def calculate_bearing_and_distance(self, x, y, landmark_pos):
        """
        Observation function to calculate the bearing and distance to a landmark
        """
        dx = landmark_pos[0] - x
        dy = landmark_pos[1] - y
        distance = np.sqrt(dx**2 + dy**2)
        bearing = np.arctan2(dy, dx)
        return bearing, distance


    def h(self, state_vector, landmarks):
        """
        Define the measurement function h(x) for the Kalman Filter
        state_vector: state vector with 3 dimensionalities: [x, y, theta]
        landmarks: list of landmark positions [(x_l1, y_l1), (x_l2, y_l2), ...]
        """
        measurements = []
        for (x_l, y_l) in landmarks:
            dx = x_l - state_vector[0]
            dy = y_l - state_vector[1]
            d = np.sqrt(dx**2 + dy**2)
            bearing = np.arctan2(dy, dx) - state_vector[2]
            measurements.extend([bearing, d])
        return np.array(measurements)


    def jacobian_c(self, state_vector, landmarks):
        """
        Calculate the Jacobian of the measurement function h(x),
        the Numerical approximation of the Jacobian
        """
        epsilon = 1e-5
        jac = np.zeros((2 * len(landmarks), len(state_vector)))
        h_x = self.h(state_vector, landmarks)
        for i in range(len(state_vector)):
            x_eps = np.copy(state_vector)
            x_eps[i] += epsilon
            h_x_eps = self.h(x_eps, landmarks)
            jac[:, i] = (h_x_eps - h_x) / epsilon
        return jac
