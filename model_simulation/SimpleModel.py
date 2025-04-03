from neuron import h


class SimpleModel:
    def __init__(self):
        props(self)
        self.topology()
        self.biophysics()

    def topology(self):
        # Create Sections
        soma = h.Section(name='soma')
        dend1 = h.Section(name='dend1')
        dend2 = h.Section(name='dend2')
        dend3 = h.Section(name='dend3')
        dend4 = h.Section(name='dend4')

        # Connect sections
        dend1.connect(soma(1))
        dend2.connect(dend1(1))
        dend3.connect(dend2(1))
        dend4.connect(dend2(1))

        # Set geometry (length in um, diameter in um)
        soma.L = soma.diam = 20
        dend1.L, dend1.diam = 100, 2
        dend2.L, dend2.diam = 100, 2
        dend3.L, dend3.diam = 50, 1.5
        dend4.L, dend4.diam = 50, 1.5

    def biophysics(self):
        # Set passive properties
        for sec in [soma, dend1, dend2, dend3, dend4]:
            sec.Ra = self.RA  # Axial resistance (ohm * cm)
            sec.cm = self.CM  # Membrane capacitance (uF/cm^2)
            sec.insert('pas')
            sec.g_pas = self.G_PAS # Passive conductance (S/cm^2)
            sec.e_pas = self.E_PAS  # Resting potential (mV)

        # Set active properties
        modpath = 'density_mechs'
        h.nrn_load_dll(modpath + '\\nrnmech.dll')

        # soma
        soma.insert('nax')
        soma.insert('kdr')
        soma.gbar_nax = self.gna_soma
        soma.gkdrbar_kdr = self.gkdr_soma

        # dendrites
        for dend in [dend1, dend2, dend3, dend4]:
            dend.insert('nad')
            dend.insert('kdr')
            dend.gbar_nad = self.gna_dend
            dend.gkdrbar_kdr = self.gkdr_dend
    
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