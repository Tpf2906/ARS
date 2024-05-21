# ann_controller.py
import numpy as np

class ANNController:
    def __init__(self, input_size, hidden_size, output_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        # Weights from input to hidden layer
        self.weights_input_hidden = np.random.randn(self.input_size, self.hidden_size)
        # Recurrent weights within the hidden layer for memory
        self.weights_hidden_hidden = np.random.randn(self.hidden_size, self.hidden_size)
        # Weights from hidden layer to output layer
        self.weights_hidden_output = np.random.randn(self.hidden_size, self.output_size)
        # Initial hidden state
        self.hidden_state = np.zeros(self.hidden_size)

    
    def forward(self, inputs):
        # Calculate the hidden state with recurrent connection
        self.hidden_state = self.sigmoid(np.dot(inputs, self.weights_input_hidden) + np.dot(self.hidden_state, self.weights_hidden_hidden))
        # Calculate the output
        output = self.sigmoid(np.dot(self.hidden_state, self.weights_hidden_output))
        return output
    
    def sigmoid(self, x):
        # Clip the values to avoid overflow
        x = np.clip(x, -500, 500)
        return 1 / (1 + np.exp(-x))
    
    def get_weights(self):
        return np.concatenate((self.weights_input_hidden.flatten(), self.weights_hidden_hidden.flatten(), self.weights_hidden_output.flatten()))
    
    def set_weights(self, weights):
        input_hidden_size = self.input_size * self.hidden_size
        hidden_hidden_size = self.hidden_size * self.hidden_size
        hidden_output_size = self.hidden_size * self.output_size

        self.weights_input_hidden = weights[:input_hidden_size].reshape((self.input_size, self.hidden_size))
        self.weights_hidden_hidden = weights[input_hidden_size:input_hidden_size + hidden_hidden_size].reshape((self.hidden_size, self.hidden_size))
        self.weights_hidden_output = weights[input_hidden_size + hidden_hidden_size:input_hidden_size + hidden_hidden_size + hidden_output_size].reshape((self.hidden_size, self.output_size))

    