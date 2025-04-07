import matplotlib.pyplot as plt

from SimpleModel import SimpleModel
from simulation import run_simulation, add_single_synapse
from neuron import h, gui


model = SimpleModel()
add_single_synapse(model, 'soma', 'AMPA', 20, loc=0.5, weight=0.0001)
t, v = run_simulation(model, 'soma', delay=20, duration=15, amplitude=0, tstop=100)

# Plot the results
plt.figure(figsize=(8, 5))
plt.plot(t, v, label="Membrane Potential (mV)", color="black")
plt.xlabel("Time (ms)")
plt.ylabel("Voltage (mV)")
plt.title("Membrane Potential")
plt.legend()
plt.show()





