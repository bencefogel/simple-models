from neuron import h


class SimpleModel:
    def __init__(self):
        # Initialize the synapse reference storage
        self._syn_refs = []

        # Set up model
        props(self)
        self.topology()
        self.biophysics()

    def topology(self):
        # Create Sections
        self.soma = h.Section(name='soma')
        self.dend1 = h.Section(name='dend1')
        self.dend2 = h.Section(name='dend2')
        self.dend3 = h.Section(name='dend3')
        self.dend4 = h.Section(name='dend4')

        # Connect sections
        self.dend1.connect(self.soma(1))
        self.dend2.connect(self.dend1(1))
        self.dend3.connect(self.dend2(1))
        self.dend4.connect(self.dend2(1))

        # Set geometry (length in um, diameter in um)
        self.soma.L = self.soma.diam = 20
        self.dend1.L, self.dend1.diam = 100, 2
        self.dend2.L, self.dend2.diam = 100, 2
        self.dend3.L, self.dend3.diam = 50, 1.5
        self.dend4.L, self.dend4.diam = 50, 1.5

    def biophysics(self):
        # Set passive properties
        for sec in [self.soma, self.dend1, self.dend2, self.dend3, self.dend4]:
            sec.Ra = self.RA  # Axial resistance (ohm * cm)
            sec.cm = self.CM  # Membrane capacitance (uF/cm^2)
            sec.insert('pas')
            sec.g_pas = self.G_PAS # Passive conductance (S/cm^2)
            sec.e_pas = self.E_PAS  # Resting potential (mV)

        # Set active properties
        modpath = 'density_mechs'
        h.nrn_load_dll(modpath + '\\nrnmech.dll')

        # soma
        self.soma.insert('nax')
        self.soma.insert('kdr')
        self.soma.gbar_nax = self.gna_soma
        self.soma.gkdrbar_kdr = self.gkdr_soma

        # dendrites
        for dend in [self.dend1, self.dend2, self.dend3, self.dend4]:
            dend.insert('nad')
            dend.insert('kdr')
            dend.gbar_nad = self.gna_dend
            dend.gkdrbar_kdr = self.gkdr_dend

    def add_synapse_ref(self, syn, stim, nc):
        """
        Adds the synapse, stimulus, and connection to the internal reference list to
        prevent garbage collection from deleting them.
        """
        self._syn_refs.append((syn, stim, nc))

def props(model):
    # Passive properties
    model.RA = 100
    model.CM = 1
    model.G_PAS = 0.0001
    model.E_PAS = -66
    # Active properties
    model.gna_soma = 0.2
    model.gkdr_soma = 0.04
    model.gna_dend = 0.03
    model.gkdr_dend = 0.02