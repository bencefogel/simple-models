import numpy as np
import pandas as pd
from neuron import h
from record_data import record_time_vector, record_membrane_potential

def run_simulation(model, inj_site='soma', delay=100, duration=500, amplitude=0.1, tstop=1000):
    """
    Run a simulation with a current injection protocol.

    Parameters:
        model: The neuron model.
        inj_site (str): The section where current is injected ('soma', 'dend1', etc.).
        delay (float): Time (ms) before current starts.
        duration (float): Duration (ms) of the current injection.
        amplitude (float): Amplitude (nA) of the injected current.
        tstop (float): Total simulation time (ms).

    Returns:
        t (numpy array): Time vector.
        v (numpy array): Voltage at the soma.
    """
    # Set fixed time-step
    h.CVode().active(False)  # Disable variable time-step solver
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

    t = record_time_vector()
    v_seg, v = record_membrane_potential()

    # Run the simulation
    h.finitialize(-64.54)
    h.continuerun(tstop)

    df_v = pd.DataFrame(data = np.array(v), index=v_seg)
    df_v.columns = list(df_v.columns)

    return np.array(t), df_v


def add_single_synapse(model, target_section, syn_type, event_time, loc=0.5, weight=0.001):
    """
    Adds a single synapse (AMPA, NMDA, GABAfast, GABAslow) to a given section at a specific time.

    Parameters:
        model: The neuron model.
        target_section (str): The section where the synapse is applied (e.g., 'soma', 'dend1').
        syn_type (str): Synapse type ('AMPA', 'NMDA', 'GABAfast', 'GABAslow').
        event_time (float): The time (ms) at which the synapse is activated.
        loc (float): Location along the section (0-1, default is 0.5).
        weight (float): Synaptic weight (default: 0.001).

    Returns:
        syn: The created synapse object.
    """
    # Get the target section
    section = getattr(model, target_section, None)
    if section is None:
        raise ValueError(f"Invalid target section: {target_section}")

    # Create the appropriate synapse
    synapse_map = {
        'AMPA': h.Exp2Syn(loc, sec=section),
        'NMDA': h.Exp2SynNMDA(loc, sec=section),
        'GABAfast': h.Exp2Syn(loc, sec=section),
        'GABAslow': h.Exp2Syn(loc, sec=section)
    }

    if syn_type not in synapse_map:
        raise ValueError(f"Invalid synapse type: {syn_type}")

    syn = synapse_map[syn_type]

    # Set time constants and gmax
    if syn_type in ['AMPA']:
        syn.tau1, syn.tau2 = 0.1, 1
        syn.e = 0
    elif syn_type in ['NMDA']:
        syn.tau1, syn.tau2 = 2, 50
        syn.e = 0
    elif syn_type in ['GABAfast']:
        syn.tau1, syn.tau2 = 0.1, 4
        syn.e = -65
    elif syn_type in ['GABAslow']:
        syn.tau1, syn.tau2 = 1, 40
        syn.e = -80

    # Create NetStim (spike generator)
    stim = h.NetStim()
    stim.start = event_time
    stim.number = 1
    stim.interval = 1
    stim.noise = 0

    # Connect NetStim to synapse
    nc = h.NetCon(stim, syn)
    nc.threshold = 0
    nc.weight[0] = weight

    model.add_synapse_ref(syn, stim, nc)  # Store references in model to prevent GC
    if weight != 0:
        print(f"Synapse added at loc {loc} on {target_section}, type {syn_type}, weight {weight}")
