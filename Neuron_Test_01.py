# -*- coding: utf-8 -*-
"""
Created on Sat Sep  2 16:22:22 2023

@author: Thomas
Okay, so this file is a test demo of a 1-d chain of neurons.
The goal is to model & plot these functions, and have them work correctly in
time domain.
"""
import math
import matplotlib.pyplot as plt

def simulate_neuron(time_step, neuron_status, input_voltage, 
                activation_voltage, base_voltage,action_voltage, 
                action_impulse, action_energy, neuron_follow_factor):
    
    neuron_voltage = neuron_status[0]
    neuron_cached_energy = neuron_status[1]
    neuron_momentum = neuron_status[2]
    
    
    if input_voltage > action_voltage:
        neuron_momentum = neuron_momentum +  (neuron_cached_energy/neuron_energy_storage) * action_impulse * time_step
        neuron_cached_energy -= (neuron_cached_energy/neuron_energy_storage) * action_impulse * time_step
        
    
        
    neuron_voltage = neuron_voltage + neuron_momentum * time_step
    neuron_momentum = 0.99 * neuron_momentum - 0.009 * (neuron_voltage - base_voltage)
    energy_used = max(0,(neuron_voltage - base_voltage) * time_step)
    neuron_cached_energy = max(0,neuron_cached_energy-energy_used)
    if neuron_cached_energy < neuron_energy_storage:
        if neuron_voltage < 0:
            neuron_cached_energy += max((5*(base_voltage - neuron_voltage)+1) * time_step,0)
        neuron_cached_energy += 5*time_step
        neuron_cached_energy = min(neuron_cached_energy,neuron_energy_storage)
        
    #neuron_momentum -= 10*(max(0,neuron_energy_storage) - max(0,neuron_cached_energy))
    #neuron_voltage = max(neuron_voltage,0)
    #neuron_momentum = (neuron_momentum - 1 )* 0.5
    
    
        
    
    print(neuron_voltage, neuron_momentum, neuron_cached_energy)
    
    
    return [neuron_voltage, neuron_cached_energy, neuron_momentum]
    
    #updates neuron cached energy.
    

def simulate_test(time_step, activation_voltage, base_voltage,
                  action_voltage, action_impulse, action_energy,
                  neuron_energy_storage, neuron_follow_factor):
    neuron_status = [base_voltage,neuron_energy_storage,0] #neuron voltage, neuron cached energy, momentum.
    
    #i is in unit ms
    time = []
    log_inputs = []
    log_outputs = []
    log_energy = []
    for i in range(5000):
        input_voltage = base_voltage+150*math.sin(i/50)
        #print(input_voltage)
        neuron_status = simulate_neuron(time_step, neuron_status, input_voltage, 
                        activation_voltage, base_voltage,action_voltage, 
                        action_impulse, action_energy, neuron_follow_factor)
        
        log_inputs.append(input_voltage)
        log_outputs.append(neuron_status[0])
        time.append(i*time_step)
        log_energy.append(neuron_status[1])
    plt.plot(time,log_inputs)
    plt.plot(time,log_outputs)
    plt.plot(time,log_energy)
    plt.show()

if __name__ == "__main__":
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
    #to the target
    simulate_test(time_step, activation_voltage, base_voltage,
                      action_voltage, action_impulse, action_energy,
                      neuron_energy_storage, neuron_follow_factor)
    
    
    
