# components/ccvs.py
# Current-Controlled Voltage Source (CCVS)

import numpy as np

from components.base import Component

class CCVS(Component):
    # Khai bao CCVS giua node i va j, dieu khien boi dong dien giua node k va l
    def __init__(self, name, np, nm, Vctrl, value):
        self.name = name
        self.n_p = np
        self.n_m = nm
        self.Vctrl = Vctrl
        self.Rm = value # Resistance


    # Mo hinh linear CCVS
    def _stamp_linear(self, G, Rm, ctx):
        if self.Vctrl not in ctx.vs_index:
            raise ValueError(f"{self.name}: control source {self.Vctrl} not found")
        
        if self.name not in ctx.vs_index:
            raise ValueError(f"{self.name}: CCVS not indexed")

        k_ctrl = ctx.vs_index[self.Vctrl]
        Ie_idx = ctx.vs_index[self.name]

        # Ma tran G
        if self.n_p is not None:
            G[self.n_p][Ie_idx] += 1
            G[Ie_idx][self.n_p] += 1

        if self.n_m is not None:
            G[self.n_m][Ie_idx] -= 1
            G[Ie_idx][self.n_m] -= 1

        G[Ie_idx][k_ctrl] -= Rm




    # Mo hinh DC
    def stamp_dc(self, G, b, ctx):
        self._stamp_linear(G, self.Rm, ctx)
    

    # Hien thi thong tin linh kien (cho debug)
    def __repr__(self):
        return f"CCVS({self.name}, {self.n_p}, {self.n_m}, {self.Vctrl}, {self.Rm}) at {hex(id(self))}"