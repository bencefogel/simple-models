import neuron
from neuron import h, gui

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

# Set passive properties
for sec in [soma, dend1, dend2, dend3, dend4]:
    sec.Ra = 100    # Axial resistance (ohm * cm)
    sec.cm = 1      # Membrane capacitance (uF/cm^2)
    sec.insert('pas')  # Insert passive mechanism
    sec.g_pas = 0.0001  # Passive conductance (S/cm^2)
    sec.e_pas = -66    # Resting potential (mV)

# Set active properties
modpath = 'density_mechs'
h.nrn_load_dll(modpath + '\\nrnmech.dll')

# soma
soma.insert('nax')
soma.insert('kdr')
gna_soma = 0.2
gkdr_soma = 0.04
soma.gbar_nax = gna_soma
soma.gkdrbar_kdr = gkdr_soma

# dendrites
gna_dend = 0.03
gkdr_dend = 0.02

for dend in [dend1, dend2, dend3, dend4]:
    dend.insert('nad')
    dend.insert('kdr')
    dend.gbar_nad = gna_dend
    dend.gkdrbar_kdr = gkdr_dend



