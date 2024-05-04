# TODO: (Tiago) please do a pylint check and fix the issues in the code.
# remove the next line to see the pylint issues
# pylint: disable=invalid-name
import numpy as np

class KalmanFilter:
    def __init__(self, A, B, C, Q, R, x, P):
        """
        Initialize the Kalman Filter
        :param A: Transition matrix
        :param B: Control-input matrix
        :param C: Observation matrix
        :param Q: Process noise covariance
        :param R: Measurement noise covariance
        :param x: Initial state estimate
        :param P: Initial error covariance
        """
        self.A = A  # State transition matrix
        self.B = B  # Control-input matrix
        self.C = C  # Observation matrix
        self.Q = Q  # Process noise covariance
        self.R = R  # Measurement noise covariance
        self.state_estimate = x  # State estimate vector
        self.error_covariance = P  # Error covariance matrix

    def predict(self, control_vector):
        """
        Prediction step of the Kalman Filter
        :param control_vector: The control input
        """
        # State prediction
        self.state_estimate = np.dot(self.A, self.state_estimate) + np.dot(self.B, control_vector)

        # Covariance prediction
        self.error_covariance = np.dot(np.dot(self.A, self.error_covariance), self.A.T) + self.Q

    def correct(self, measurement_vector, landmarks):
        """
        Correction step of the Kalman Filter
        :param measurement_vector: The measurement input
        """
        C = self.jacobian_C(self.state_estimate, landmarks)

        # Kalman Gain calculation
        S = np.dot(C, np.dot(self.error_covariance, C.T)) + self.R
        kalman_gain = np.dot(np.dot(self.error_covariance, C.T), np.linalg.inv(S))

        y = measurement_vector - self.h(self.state_estimate, landmarks)

        # State update
        self.state_estimate = self.state_estimate + np.dot(kalman_gain, y)

        # Covariance update
        identity_matrix = np.eye(self.A.shape[0])
        self.error_covariance = np.dot((identity_matrix - np.dot(kalman_gain, C)),
                                        self.error_covariance)

    def get_state_estimate(self):
        """
        Get the current state estimate
        """
        return self.state_estimate

    def calculate_bearing_and_distance(self, x, y, landmark_pos):
        """
        Observation function to calculate the bearing and distance to a landmark
        """
        dx = landmark_pos[0] - x
        dy = landmark_pos[1] - y
        distance = np.sqrt(dx**2 + dy**2)
        bearing = np.arctan2(dy, dx)
        return bearing, distance

    def h(self, x, landmarks):
        """
        Define the measurement function h(x) for the Kalman Filter
        x: state vector [x, y, theta]
        landmarks: list of landmark positions [(x_l1, y_l1), (x_l2, y_l2), ...]
        """
        measurements = []
        for (x_l, y_l) in landmarks:
            dx = x_l - x[0]
            dy = y_l - x[1]
            d = np.sqrt(dx**2 + dy**2)
            bearing = np.arctan2(dy, dx) - x[2]
            measurements.extend([bearing, d])
        return np.array(measurements)

    def jacobian_C(self, x, landmarks):
        """
        Calculate the Jacobian of the measurement function h(x),
        the Numerical approximation of the Jacobian
        """
        epsilon = 1e-5
        jac = np.zeros((2 * len(landmarks), len(x)))
        h_x = self.h(x, landmarks)
        for i in range(len(x)):
            x_eps = np.copy(x)
            x_eps[i] += epsilon
            h_x_eps = self.h(x_eps, landmarks)
            jac[:, i] = (h_x_eps - h_x) / epsilon
        return jac
