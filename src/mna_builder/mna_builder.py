# mna_builder/mna_builder.py

import numpy as np

from mna_builder.stamp_context import StampContext

from components.resistor import Resistor
from components.voltage_source import VoltageSource
from components.vcvs import VCVS
from components.ccvs import CCVS

class MNABuilder:
    def __init__(self, circuit):
        self.circuit = circuit
        self.node_map = circuit.node_map
        self.vs_index = self.build_vs_index()


    def build_vs_index(self):
        vs_list = []
        vs_index = {}

        # Liet ke cac nguon ap (VoltageSource, CCVS, VCVS)
        for comp in self.circuit.components:
            if isinstance(comp, (VoltageSource, VCVS, CCVS)):
                vs_list.append(comp)

        # Tao index cho nguon ap trong vector x
        base = len(self.node_map) # So node khong tinh GND
        for k, vs in enumerate(vs_list):
            vs_index[vs.name] = base + k

        return vs_index


    def build_dc(self):
        n = len(self.node_map) # So node (khong tinh GND)
        m = len(self.vs_index) # So bien dong cua nguon ap
        size = n + m

        # Tao ma tran G, vector b
        G = np.zeros((size, size))
        b = np.zeros(size)

        # Lay noi dung context cua linh kien
        ctx = StampContext(self.vs_index)

        # Duyet linh kien vao ma tran
        for comp in self.circuit.components:
            comp.stamp_dc(G, b, ctx)

        # In ma tran G, vector b, index cua nguon ap (cho debug)
        print("G =\n", G)
        print("b =\n", b)
        print("vs_index =\n",self.vs_index)

        return G, b
