'''
This file contains the implementation of the controller for the Artificial Neural Network (ANN) 
that will be used to control the agent in the environment. The controller is implemented as a 
class that contains the weights of the network and the forward pass function. The forward pass 
function calculates the output of the network given the input. The controller also contains functions 
to get and set the weights of the network. The weights are stored as a single numpy array for easy manipulation.
'''
import numpy as np

class ANNController:
    '''
    Controller for the ANN that will be used to control the agent in the environment.
    '''
    def __init__(self, input_size, hidden_size, output_size):
        '''
        Initialize the controller with the given input, hidden, and output sizes.
        '''
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
        '''
        Calculate the output of the network given the input.
        '''
        # Calculate the hidden state with recurrent connection
        self.hidden_state = self.sigmoid(np.dot(inputs, self.weights_input_hidden) + np.dot(self.hidden_state, self.weights_hidden_hidden))
        # Calculate the output
        output = self.sigmoid(np.dot(self.hidden_state, self.weights_hidden_output))
        return output
    
    
    def sigmoid(self, x):
        '''
        Sigmoid activation function.
        '''
        # Clip the values to avoid overflow
        x = np.clip(x, -500, 500)
        return 1 / (1 + np.exp(-x))
    
    
    def get_weights(self):
        '''
        Get the weights of the network as a single numpy array.
        '''
        return np.concatenate((self.weights_input_hidden.flatten(), self.weights_hidden_hidden.flatten(), self.weights_hidden_output.flatten()))
    
    
    def set_weights(self, weights):
        '''
        Set the weights of the network from a single numpy array.
        '''
        input_hidden_size = self.input_size * self.hidden_size
        hidden_hidden_size = self.hidden_size * self.hidden_size
        hidden_output_size = self.hidden_size * self.output_size

        self.weights_input_hidden = weights[:input_hidden_size].reshape((self.input_size, self.hidden_size))
        self.weights_hidden_hidden = weights[input_hidden_size:input_hidden_size + hidden_hidden_size].reshape((self.hidden_size, self.hidden_size))
        self.weights_hidden_output = weights[input_hidden_size + hidden_hidden_size:input_hidden_size + hidden_hidden_size + hidden_output_size].reshape((self.hidden_size, self.output_size))

    