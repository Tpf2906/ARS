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
        self.error_covariance = np.dot(np.dot(self.A, self.error_covariance), self.A.T) + self.R

    def correct(self, measurement_vector):
        """
        Correction step of the Kalman Filter
        :param measurement_vector: The measurement input
        """
        # Kalman Gain calculation
        S = np.dot(self.C, np.dot(self.error_covariance, self.C.T)) + self.Q
        Kalman_Gain = np.dot(np.dot(self.error_covariance, self.C.T), np.linalg.inv(S))
        
        # State update
        self.state_estimate = self.state_estimate + np.dot(Kalman_Gain, (measurement_vector - np.dot(self.C, self.state_estimate)))
        
        # Covariance update
        identity_matrix = np.eye(self.A.shape[0])
        self.error_covariance = np.dot((identity_matrix - np.dot(Kalman_Gain, self.C)), self.error_covariance)

    def get_state_estimate(self):
        """
        Get the current state estimate
        """
        return self.state_estimate