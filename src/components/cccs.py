# components/cccs.py
# Current-Controlled Current Source (CCCS)

import numpy as np

from components.base import Component

class CCCS(Component):
    # Khai bao CCCS giua node i va j, dieu khien boi dong dien giua node k va l
    def __init__(self, name, np, nm, Vctrl, value):
        self.name = name
        self.n_p = np
        self.n_m = nm
        self.Vctrl = Vctrl
        self.A = value # Current gain


    # Mo hinh DC
    def stamp_dc(self, G, b, ctx):
        # Ma tran dan anp G
        k_ctrl = ctx.vs_index[self.Vctrl]

        if self.n_p is not None:
            G[self.n_p][k_ctrl] += self.A

        if self.n_m is not None:
            G[self.n_m][k_ctrl] -= self.A

    

    # Hien thi thong tin linh kien (cho debug)
    def __repr__(self):
        return f"CCCS({self.name}, {self.n_p}, {self.n_m}, {self.Vctrl}, {self.A}) at {hex(id(self))}"