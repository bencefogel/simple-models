import os
import pandas as pd
import numpy as np
from neuron import h


def measure_AMPA_current(model):
    """
    Measures AMPA receptor-mediated synaptic currents.

    Parameters:
        model (object): The NEURON model containing a list of AMPA synapses (`AMPAlist`).

    Returns:
        tuple:
            - AMPA (list): A list of `h.Vector` objects recording AMPA currents.
            - AMPA_segments (list): A list of segments where AMPA currents are recorded.
    """
    AMPA = []
    AMPA_segments = []

    for syn in model.AMPAlist:
        vec = h.Vector().record(syn._ref_i)
        AMPA.append(vec)
        AMPA_segments.append(syn.get_segment())
    return AMPA, AMPA_segments


def measure_NMDA_current(model):
    NMDA = []
    NMDA_segments = []

    for syn in model.NMDAlist:
        vec = h.Vector().record(syn._ref_i)
        NMDA.append(vec)
        NMDA_segments.append(syn.get_segment())
    return NMDA, NMDA_segments


def measure_GABA_current(model):
    GABA = []
    GABA_segments = []

    for syn in model.GABAlist:
        vec = h.Vector().record(syn._ref_i)
        GABA.append(vec)
        GABA_segments.append(syn.get_segment())
    return GABA, GABA_segments


def measure_GABA_B_current(model):
    GABA_B = []
    GABA_B_segments = []

    for syn in model.GABA_Blist:
        vec = h.Vector().record(syn._ref_i)
        GABA_B.append(vec)
        GABA_B_segments.append(syn.get_segment())
    return GABA_B, GABA_B_segments


def record_synaptic_currents(model):
    """
    Records synaptic currents for all synapse types (AMPA, NMDA, GABA, GABA-B).

    Parameters:
        model (object): The NEURON model containing lists of synapses (`AMPAlist`, `NMDAlist`, `GABAlist`, `GABA_Blist`).

    Returns:
        tuple:
            - synaptic_segments (dict): A dictionary where keys are synapse types and values are lists of segments.
            - synaptic_currents (dict): A dictionary where keys are synapse types and values are lists of `h.Vector` objects.
    """
    AMPA, AMPA_segments = measure_AMPA_current(model)
    NMDA, NMDA_segments = measure_NMDA_current(model)
    GABA, GABA_segments = measure_GABA_current(model)
    GABA_B, GABA_B_segments = measure_GABA_B_current(model)

    synaptic_currents = {
        'AMPA': AMPA,
        'NMDA': NMDA,
        'GABA': GABA,
        'GABA_B': GABA_B
    }

    synaptic_segments = {
        'AMPA': AMPA_segments,
        'NMDA': NMDA_segments,
        'GABA': GABA_segments,
        'GABA_B': GABA_B_segments
    }
    return synaptic_segments, synaptic_currents


def preprocess_synaptic_data(synaptic_segments, synaptic_currents):
    segment_dict = {}
    current_dict = {}
    for synapse_type in synaptic_segments.keys():
        segments_array = np.array(synaptic_segments[synapse_type]).astype('str')
        currents_array = np.array(synaptic_currents[synapse_type])

        segment_dict[synapse_type] = segments_array
        current_dict[synapse_type] = currents_array
    return segment_dict, current_dict
