import os
import matplotlib.pyplot as plt
from neuron import h, gui
from model_simulation.SimpleModel import SimpleModel
from model_simulation.simulation import run_simulation, add_single_synapse
from preprocessor.Preprocessor import Preprocessor
from datasaver.DataSaver import DataSaver

output_directory = 'output'

model = SimpleModel()
add_single_synapse(model, 'soma', 'NMDA', 20, loc=0.5, weight=0)

# run simulation and save data
simulation_data = run_simulation(model, 'soma', delay=20, duration=1, amplitude=0.1, tstop=100)

# preprocess_data
preprocessor = Preprocessor(simulation_data)
im = preprocessor.preprocess_membrane_currents()
iax = preprocessor.preprocess_axial_currents()

# save results
preprocessed_im_directory = 'preprocessed/im'
preprocessed_iax_directory = 'preprocessed/iax'
preprocessed_datasaver = DataSaver(columns_in_chunk=100)
preprocessed_datasaver.save_in_chunks(im, os.path.join(output_directory, preprocessed_im_directory), 'im')
preprocessed_datasaver.save_in_chunks(iax, os.path.join(output_directory, preprocessed_iax_directory), 'iax')
preprocessed_datasaver.save_time_axis(output_directory + '/taxis', simulation_data['taxis'])

