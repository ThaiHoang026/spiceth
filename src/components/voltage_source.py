# components/voltage_source.py

import numpy as np
from components.base import Component


class VoltageSource(Component):
    # Khai bao nguon ap V giua node i va j
    def __init__(self, name, node_i, node_j,
                dc_value=None,
                ac_value=None,
                transient=None):
        
        self.name = name
        self.i = node_i
        self.j = node_j
        
        self.dc = dc_value
        self.ac = ac_value
        self.transient = transient


    # Mo hinh linear voltage
    # Mo hinh DC
    def _stamp_linear(self, G, b, value, ctx):
        if self.name not in ctx.vs_index:
            raise ValueError(f"{self.name}: Voltage source not indexed")

        k = ctx.vs_index[self.name]
        # Ma tran dan nap G
        if self.i != None:
            G[self.i][k] += 1
            G[k][self.i] += 1

        if self.j != None:
            G[self.j][k] -= 1
            G[k][self.j] -= 1

        # Vector nguon input
        b[k] += value
    

    # Mo hinh DC
    def stamp_dc(self, G, b, ctx):
        self._stamp_linear(G, b, self.dc, ctx)


    # Mo hinh AC
    def stamp_ac(self, G, b, ctx):
        self._stamp_linear(G, b, self.ac, ctx)



    # Hien thi thong tin linh kien (cho debug)
    def __repr__(self):
        return f"VoltageSource({self.name}, {self.i}, {self.j}, {self.dc}, {self.ac}, {self.transient}) at {hex(id(self))}"