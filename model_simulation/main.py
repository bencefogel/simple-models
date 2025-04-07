import matplotlib.pyplot as plt

from SimpleModel import SimpleModel
from simulation import run_simulation, add_single_synapse
from neuron import h, gui


model = SimpleModel()
add_single_synapse(model, 'soma', 'NMDA', 20, loc=0.5, weight=0)
simulation_data = run_simulation(model, 'soma', delay=20, duration=1, amplitude=0.1, tstop=100)
