from neuron import h
import numpy as np


def run_simulation(model, inj_site:'soma', delay=100, duration=500, amplitude=0.1, tstop=1000):
    """
    Run a simulation with a current injection protocol.

    Parameters:
        model (SimpleModel): The neuron model.
        inj_site (str): The section where current is injected ('soma', 'dend1', etc.).
        delay (float): Time (ms) before current starts.
        duration (float): Duration (ms) of the current injection.
        amplitude (float): Amplitude (nA) of the injected current.
        tstop (float): Total simulation time (ms).
    """
    # Set fixed time-step
    h.CVode().active(False)  # disable variable time-step solver
    h.dt = 0.2  # ms

    # Get the section object from the model
    section = getattr(model, inj_site, None)
    if section is None:
        raise ValueError(f"Invalid injection site: {inj_site}")

    # Create a current clamp
    stim = h.IClamp(section(0.5))  # Inject at the middle of the section
    stim.delay = delay
    stim.dur = duration
    stim.amp = amplitude

    # Setup recording variables
    t = h.Vector().record(h._ref_t)  # Time
    v = h.Vector().record(model.soma(0.5)._ref_v)  # Voltage at soma

    # Run the simulation
    h.finitialize(-64.54)
    h.continuerun(tstop)

    return np.array(t), np.array(v)
