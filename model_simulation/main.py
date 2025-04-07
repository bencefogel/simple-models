import matplotlib.pyplot as plt

from SimpleModel import SimpleModel
from simulation import run_simulation, add_single_synapse
from neuron import h, gui

plot = False

model = SimpleModel()
add_single_synapse(model, 'soma', 'AMPA', 20, loc=0.5, weight=0)
t, df_v = run_simulation(model, 'soma', delay=20, duration=1, amplitude=0.1, tstop=100)

if plot:
    # Plot the results
    plt.figure(figsize=(8, 5))
    plt.plot(t, df_v.iloc[0, :], label="Membrane Potential (mV)", color="black")
    plt.xlabel("Time (ms)")
    plt.ylabel("Voltage (mV)")
    plt.title("Membrane Potential")
    plt.legend()
    plt.show()





