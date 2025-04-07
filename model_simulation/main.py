import matplotlib.pyplot as plt
from neuron import h, gui
from SimpleModel import SimpleModel
from simulation import run_simulation, add_single_synapse
from preprocessor.Preprocessor import Preprocessor



model = SimpleModel()
add_single_synapse(model, 'soma', 'NMDA', 20, loc=0.5, weight=0)

# run simulation and save data
simulation_data = run_simulation(model, 'soma', delay=20, duration=1, amplitude=0.1, tstop=100)

# preprocess_data
preprocessor = Preprocessor(simulation_data)
im = preprocessor.preprocess_membrane_currents()
iax = preprocessor.preprocess_axial_currents()