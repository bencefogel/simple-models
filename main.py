import os
import numpy as np
import matplotlib.pyplot as plt
from neuron import h, gui
from model_simulation.SimpleModel import SimpleModel
from model_simulation.simulation import run_simulation, add_single_synapse
from preprocessor.Preprocessor import Preprocessor
from datasaver.DataSaver import DataSaver
from currentscape_calculator.CurrentscapeCalculator import CurrentscapeCalculator

target = 'soma'
partitioning_strategy = 'type'
output_directory = 'output'

# build model
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
preprocessed_datasaver = DataSaver(columns_in_chunk=None)
preprocessed_datasaver.save_in_chunks(im, os.path.join(output_directory, preprocessed_im_directory), 'im')
preprocessed_datasaver.save_in_chunks(iax, os.path.join(output_directory, preprocessed_iax_directory), 'iax')
preprocessed_datasaver.save_time_axis(output_directory + '/taxis', simulation_data['taxis'])

# partition axial currents
regions_list_directory = 'currentscape_calculator/regions'
currentscape_calculator = CurrentscapeCalculator(target, partitioning_strategy, regions_list_directory)
input_directory = os.path.join(output_directory, 'preprocessed')
iax_file = os.path.join(input_directory, 'iax', 'current_values_0_328.csv')
im_file = os.path.join(input_directory, 'im', 'current_values_0_328.csv')

im_part_pos, im_part_neg = currentscape_calculator.calculate_currentscape(iax_file, im_file, timepoints=None)

part_pos_sum = im_part_pos.sum().values
part_neg_sum = im_part_neg.sum().values

# sanity check
t = simulation_data['taxis']
plt.figure()
plt.plot(t, part_pos_sum+part_neg_sum)
plt.show()
