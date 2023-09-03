# -*- coding: utf-8 -*-
"""
Created on Sat Sep  2 16:22:22 2023

@author: Thomas Warnasch
Okay, so this file is a test demo of a 1-d chain of neurons.
The goal is to model & plot these functions, and have them work correctly in
time domain.
"""
import math
import matplotlib.pyplot as plt

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
    
    #updates neuron cached energy.
    

def simulate_test(time_step, activation_voltage, base_voltage,
                  action_voltage, action_impulse, action_energy,
                  neuron_energy_storage, neuron_follow_factor,
                  default_utilization, utilization_gain_rate,
                  utilization_decay_rate):
    neuron_status = [base_voltage,neuron_energy_storage,0,default_utilization] #neuron voltage, neuron cached energy, momentum.
    
    #i is in unit ms
    time = []
    log_inputs = []
    log_outputs = []
    log_energy = []
    log_neuron_utilization = []
    for i in range(50000):
        input_voltage = base_voltage+150*math.sin(i/600)
        #print(input_voltage)
        neuron_status = simulate_neuron(time_step, neuron_status, input_voltage, 
                        activation_voltage, base_voltage,action_voltage, 
                        action_impulse, action_energy, neuron_follow_factor,
                        utilization_gain_rate, utilization_decay_rate)
        
        log_inputs.append(input_voltage)
        log_outputs.append(neuron_status[0])
        time.append(i*time_step)
        log_energy.append(neuron_status[1])
        log_neuron_utilization.append(neuron_status[3]*100)
        
    plt.plot(time,log_inputs)
    plt.plot(time,log_outputs)
    plt.plot(time,log_energy)
    plt.plot(time,log_neuron_utilization)
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
    default_utilization = 0.5
    utilization_gain_rate = 0.025
    utilization_decay_rate = 0.00005
    #to the target
    simulate_test(time_step, activation_voltage, base_voltage,
                      action_voltage, action_impulse, action_energy,
                      neuron_energy_storage, neuron_follow_factor,
                      default_utilization, utilization_gain_rate,
                      utilization_decay_rate)
    
    
    
