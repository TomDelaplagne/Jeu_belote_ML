import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.weights_input_to_hidden = np.random.normal(0, self.input_size**-0.5, 
                                       (self.input_size, self.hidden_size))
        self.weights_hidden_to_output = np.random.normal(0, self.hidden_size**-0.5, 
                                       (self.hidden_size, self.output_size))
        self.hidden_bias = np.zeros(self.hidden_size)
        self.output_bias = np.zeros(self.output_size)

    def train(self, inputs, targets, learning_rate=0.5):
        inputs = inputs.reshape(self.input_size, 1)
        targets = targets.reshape(self.output_size, 1)

        hidden_inputs = np.dot(self.weights_input_to_hidden.T, inputs) + self.hidden_bias
        hidden_outputs = sigmoid(hidden_inputs)
        final_inputs = np.dot(self.weights_hidden_to_output.T, hidden_outputs) + self.output_bias
        final_outputs = sigmoid(final_inputs)

        output_error = targets - final_outputs
        hidden_error = np.dot(self.weights_hidden_to_output, output_error)
        
        self.weights_hidden_to_output += learning_rate * np.dot(hidden_outputs, output_error.T)
        self.weights_input_to_hidden += learning_rate * np.dot(inputs, hidden_error.T)
        self.hidden_bias += learning_rate * np.sum(hidden_error, axis=1, keepdims=True)
        self.output_bias += learning_rate * np.sum(output_error, axis=1, keepdims=True)

    def predict(self, inputs):
        inputs = inputs.reshape(self.input_size, 1)

        hidden_inputs = np.dot(self.weights_input_to_hidden.T, inputs) + self.hidden_bias
        hidden_outputs = sigmoid(hidden_inputs)
        final_inputs = np.dot(self.weights_hidden_to_output.T, hidden_outputs) + self.output_bias
        final_outputs = sigmoid(final_inputs)

        return final_outputs
