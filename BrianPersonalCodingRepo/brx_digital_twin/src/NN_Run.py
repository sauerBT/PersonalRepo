# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 15:07:55 2019

@author: bsauer
"""
import numpy as np
import matplotlib.pyplot as plt
#from scipy import ndimage
from NN_Helper import *
### CONSTANTS ###

def L_layer_model(X, Y, layers_dims, learning_rate = 0.0075, num_iterations = 3000, print_cost=False, lambd = 0):#lr was 0.009
    """
    Implements a L-layer neural network: [LINEAR->RELU]*(L-1)->LINEAR->SIGMOID.
    
    Arguments:
    X -- data, numpy array of shape (number of examples, num_px * num_px * 3)
    Y -- true "label" vector (containing 0 if cat, 1 if non-cat), of shape (1, number of examples)
    layers_dims -- list containing the input size and each layer size, of length (number of layers + 1).
    learning_rate -- learning rate of the gradient descent update rule
    num_iterations -- number of iterations of the optimization loop
    print_cost -- if True, it prints the cost every 100 steps
    
    Returns:
    parameters -- parameters learnt by the model. They can then be used to predict.
    """

    np.random.seed(1)
    costs = []                         # keep track of cost
    
    # Parameters initialization.
    parameters = initialize_parameters_deep(layers_dims)
    
    # Loop (gradient descent)
    for i in range(0, num_iterations):   
        # Forward propagation: [LINEAR -> RELU]*(L-1) -> LINEAR -> SIGMOID.
        AL, caches = L_model_forward(X, parameters)
        
        # Compute cost.
        cost = compute_cost_with_regularization(AL, Y, parameters, lambd)
    
        # Backward propagation.
        grads = L_model_backward_with_regularization(AL, Y, caches, lambd)

        # Update parameters.
        parameters = update_parameters(parameters, grads, learning_rate)
                
        # Print the cost every 100 training example
        if print_cost and i % 100 == 0:
            print ("Cost after iteration %i: %f" %(i, cost))
        if print_cost and i % 100 == 0:
            costs.append(cost)
            # plot output vs input
            x1 = np.linspace(0,AL.shape[1], num=AL.shape[1])
            x2 = np.linspace(0,Y.shape[1], num=Y.shape[1])
            # print(AL)
            plt.figure(0)
            plt.plot(x2,Y.T, 'yo', markersize=.07)
            plt.plot(x1,AL.T, 'ko', markersize=.07)
            plt.ylabel('Filtered Rate')
            plt.xlabel('Data Points')
            plt.title("Learned Filter")
            plt.show()
           
    # plot the cost
    plt.figure(1)
    plt.plot(np.squeeze(costs))
    plt.ylabel('cost')
    plt.xlabel('iterations (per tens)')
    plt.title("Learning rate =" + str(learning_rate))
    plt.show()
    
    return parameters, AL