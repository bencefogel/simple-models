from neuron import h
import numpy as np


def record_time_vector():
    t = h.Vector().record(h._ref_t)
    return t

def record_membrane_potential():
    """
    Records the membrane potential from all segments in all sections of the NEURON model.

    Returns:
        tuple:
            - v_segments (list): A list of segment objects where the membrane potential was recorded.
            - v (list): A list of `h.Vector` objects containing the recorded membrane potential data.
    """
    v = []
    v_segments = []

    for sec in h.allsec():
        for seg in sec.allseg():
            v_segments.append(seg)
            v.append(h.Vector().record(seg._ref_v))
    return v_segments, v

def preprocess_membrane_potential_data(v_segments, v):
    segments_array = np.array([str(seg) for seg in v_segments])
    potential_array = np.array(v)
    return segments_array, potential_array
