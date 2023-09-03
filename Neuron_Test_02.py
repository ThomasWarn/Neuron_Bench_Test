# -*- coding: utf-8 -*-
"""
Created on Sat Sep  2 16:31:24 2023

@author: Thomas Warnasch
"""

import numpy as np
import random
import math

def import_training_data():
    #for now learning to correlate inputs to outputs with no fancy buisness.
    #basically 1 == 1, 2 == 2, and stuff like that.

    data_pairs = []
    for i in range(9999):
        inputs = [0,0,0,0,0,0,0,0,0,0]
        inputs[random.randint(0,9)] = 1
        outputs = inputs
        data_pairs.append([inputs,outputs])
    return data_pairs

def simulate_neuron(time_step, neuron_status, input_voltage, 
                activation_voltage, base_voltage,action_voltage, 
                action_impulse, action_energy, neuron_follow_factor, 
                utilization_gain_rate, utilization_decay_rate):
    
    neuron_voltage = neuron_status[0]
    neuron_cached_energy = neuron_status[1]
    neuron_momentum = neuron_status[2]
    neuron_utilization = neuron_status[3]
    
    if input_voltage > action_voltage and neuron_cached_energy/neuron_energy_storage > 0.5:
        neuron_utilization = (1-utilization_gain_rate) * neuron_utilization + utilization_gain_rate
    else:
        neuron_utilization = (1-utilization_decay_rate) * neuron_utilization
    if input_voltage > action_voltage:
        neuron_momentum = neuron_momentum +  (neuron_cached_energy/neuron_energy_storage) * action_impulse * time_step
        neuron_cached_energy -= (neuron_cached_energy/neuron_energy_storage) * action_impulse * time_step
        #Only counted as utilized if energy is more than half full.
    
        
        
    
        
    neuron_voltage = neuron_voltage + neuron_momentum * time_step
    neuron_momentum = 0.99 * neuron_momentum - 0.009 * (neuron_voltage - base_voltage)
    energy_used = max(0,(neuron_voltage - base_voltage) * time_step)
    neuron_cached_energy = max(0,neuron_cached_energy-energy_used)
    if neuron_cached_energy < neuron_energy_storage:
        if neuron_voltage < 0:
            neuron_cached_energy += max((5*(base_voltage - neuron_voltage)+1) * time_step,0)
        neuron_cached_energy += 5*time_step
        neuron_cached_energy = min(neuron_cached_energy,neuron_energy_storage)
    
    #print(neuron_voltage, neuron_momentum, neuron_cached_energy)
    
    
    return [neuron_voltage, neuron_cached_energy, neuron_momentum, neuron_utilization]

def perform_assertions(network_inputs,network_inputs_size,network_inputs_location,network_outputs,network_outputs_size,network_outputs_location,network_length,network_height,network_depth):
    assert network_inputs_size[2] == 1,'Must be 1, otherwise connections will be difficult.'
    assert network_inputs_size[0]*network_inputs_size[1]*network_inputs_size[2]>= network_inputs,'Not enough space to fit all inputs'
    assert network_inputs_location[0] <= network_length,'input mask orgin out of bounds'
    assert network_inputs_location[1] <= network_height,'input mask orgin out of bounds'
    assert network_inputs_location[2] <= network_depth,'input mask orgin out of bounds'
    assert network_inputs_location[0] + network_inputs_size[0] <= network_length,'input mask out of bounds'
    assert network_inputs_location[1] + network_inputs_size[1] <= network_height,'input mask out of bounds'
    assert network_inputs_location[2] + network_inputs_size[2] <= network_depth,'input mask out of bounds'

    assert network_outputs_size[2] == 1,'Must be 1, otherwise connections will be difficult.'
    assert network_outputs_size[0]*network_outputs_size[1]*network_outputs_size[2]>= network_outputs,'Not enough space to fit all outputs'
    assert network_outputs_location[0] <= network_length,'outputs mask orgin out of bounds'
    assert network_outputs_location[1] <= network_height,'outputs mask orgin out of bounds'
    assert network_outputs_location[2] <= network_depth,'outputs mask orgin out of bounds'
    assert network_outputs_location[0] + network_outputs_size[0] <= network_length,'outputs mask out of bounds'
    assert network_outputs_location[1] + network_outputs_size[1] <= network_height,'outputs mask out of bounds'
    assert network_outputs_location[2] + network_outputs_size[2] <= network_depth,'outputs mask out of bounds'

def create_new_base_network(network_length, network_height, network_depth):
    network_energy = np.random.rand(network_length, network_height, network_depth)
    network_weights = np.random.rand(network_length, network_height, network_depth)
    network_biases = np.random.rand(network_length, network_height, network_depth)
    #connecting to 8 neurons if network_depth is 1, otherwise connecting to 17 if depth is 2 & 16 if depth is 3.
    if network_depth == 1:
        network_connections = np.random.rand(network_length, network_height, network_depth,8)
    elif network_depth == 2:
        network_connections = np.random.rand(network_length, network_height, network_depth,17)
    elif network_depth >=3:
        network_connections = np.random.rand(network_length, network_height, network_depth,26)
    network_state = np.zeros((network_length, network_height, network_depth))
    return network_energy, network_connections, network_state, network_weights, network_biases

if __name__ == "__main__":
    network_inputs = 10 #How many input nodes there are into the network.
    network_inputs_size = (2,5,1) #the shape of the inputs. It could be a line, or it could be a pad. Padded to be rectangular.
    network_inputs_location = (3,3,0)#top left corner of where the network inputs are
    network_outputs = 10 #How many output nodes there are out of the network.
    network_outputs_size = (2,5,1)#shape of the outputs, padded to be rectangular.
    network_outputs_location = (5,5,2)
    network_length = 10
    network_height = 10
    network_depth = 3
    perform_assertions(network_inputs,network_inputs_size,network_inputs_location,network_outputs,network_outputs_size,network_outputs_location,network_length,network_height,network_depth)
    cycles_per_training_period = 100 #information takes time to move through the network. This is how many itterations will be computed before results are expected
    
    #Simulation parameters
    time_step = 0.01 #simulated milliseconds, arbritary realistically.
    #Biology parameters based on https://en.wikipedia.org/wiki/Action_potential
    activation_voltage = 20 #mv
    base_voltage = 0 #mv
    action_voltage = 100 #mv, the threshold for activation
    action_impulse = 1000 #mv/ms, or volt /sec, how quickly voltage increases
    action_energy = 100 #mv-ms
    neuron_energy_storage = 200 #mv-ms
    neuron_follow_factor = 0.5 #each step the neuron will be this ratio closer
    default_utilization = 0.5
    utilization_gain_rate = 0.025
    utilization_decay_rate = 0.00005

    network_energy, network_connections, network_state, network_weights, network_biases = create_new_base_network(network_length, network_height, network_depth)
    training_pairs = import_training_data()
    
    
    #to train a model we need a predict function, an evaluation function, and a train function.
    #Start with random values, so let's just evaluate and see what our results are.
    input_info = [network_inputs,network_inputs_size,network_inputs_location]
    output_info = [network_outputs, network_outputs_size, network_outputs_location]
    model_predict(inputs, input_info, output_info,network_energy, 
                  network_connections, network_state, 
                  network_weights, network_biases,time_step, activation_voltage, 
                  base_voltage, action_voltage, action_impulse, action_energy,
                  neuron_energy_storage, neuron_follow_factor, default_utilization,
                  utilization_gain_rate, utilization_decay_rate)
    
    
    
    
    
    