# mna_builder/mna_builder.py

import numpy as np

from mna_builder.stamp_context import StampContext
from components.voltage_source import VoltageSource
from components.inductor import Inductor
from components.vcvs import VCVS
from components.ccvs import CCVS

# f = 100 # Frequency (Hz)
# omega = 2 * np.pi * f
# omega = 2

class MNABuilder:
    def __init__(self, circuit):
        self.circuit = circuit
        self.node_map = circuit.node_map


    def build_vs_index(self, mode):
        vs_list = []
        vs_index = {}

        # Liet ke cac nguon ap (VoltageSource, CCVS, VCVS), Inductor o DC coi nhu la short-circuit (VS = 0)
        for comp in self.circuit.components:
            if isinstance(comp, (VoltageSource, VCVS, CCVS)):
                vs_list.append(comp)

            elif isinstance(comp, Inductor) and mode == "dc":
                vs_list.append(comp)

        # Tao index cho nguon ap trong vector x
        base = len(self.node_map) # So node khong tinh GND
        for k, vs in enumerate(vs_list):
            vs_index[vs.name] = base + k

        return vs_index


    # Ma tran tuyen tinh
    def build_linear(self, mode="dc", omega=0.0):
        self.vs_index = self.build_vs_index(mode)

        n = len(self.node_map) # So node (khong tinh GND)
        m = len(self.vs_index) # So bien dong cua nguon ap
        size = n + m

        # Kieu du lieu cho mode dc va ac
        dtype = complex if mode == "ac" else float

        # Tao ma tran G, vector b
        G = np.zeros((size, size), dtype=dtype)
        b = np.zeros(size, dtype=dtype)

        # Duyet linh kien vao ma tran
        ctx = StampContext(self.vs_index, omega)
        
        for comp in self.circuit.components:
            if mode == "dc":
                comp.stamp_dc(G, b, ctx)
            elif mode == "ac":
                comp.stamp_ac(G, b, ctx)

                          
        # In ma tran G, vector b, index cua nguon ap (cho debug)
        print("G =\n", G)
        print("b =\n", b)
        print("vs_index =\n",self.vs_index)

        return G, b


    # Build DC matrix
    def build_dc(self):
        return self.build_linear(mode="dc", omega=0)


    # Build AC matrix
    def build_ac(self, omega):
        return self.build_linear(mode="ac", omega=omega)