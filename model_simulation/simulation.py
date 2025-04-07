import numpy as np
from neuron import h

from recording_utils import record_time_vector, record_membrane_potential, preprocess_membrane_potential_data
from model_simulation.record_intrinsic import  record_intrinsic_currents, preprocess_intrinsic_data
from model_simulation.record_synaptic import record_synaptic_currents, preprocess_synaptic_data

def run_simulation(model, inj_site='soma', delay=100, duration=500, amplitude=0.1, tstop=1000):
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

    # Record data
    t = record_time_vector()
    v_seg, v = record_membrane_potential()
    intrinsic_seg, intrinsic_currents = record_intrinsic_currents()
    synaptic_seg, synaptic_currents = record_synaptic_currents(model)

    # Run the simulation
    h.finitialize(-64.54)
    h.continuerun(tstop)

    # preprocess time axis
    taxis = np.array(t)

    # preprocess voltage data
    v_segments, v_arrays = preprocess_membrane_potential_data(v_seg, v)
    intrinsic_segments, intrinsic_arrays = preprocess_intrinsic_data(intrinsic_seg, intrinsic_currents)
    synaptic_segments, synaptic_arrays = preprocess_synaptic_data(synaptic_seg, synaptic_currents)

    simulation_data = {'membrane_potential_data': [v_segments, v_arrays],
                       'intrinsic_data': [intrinsic_segments, intrinsic_arrays],
                       'synaptic_data': [synaptic_segments, synaptic_arrays],
                       'taxis': taxis}
    return simulation_data


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
