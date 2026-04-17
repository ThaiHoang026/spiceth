# components/vcvs.py
# Voltage-Controlled Voltage Source (VCVS)

import numpy as np

from components.base import Component

class VCVS(Component):
    # Khai bao VCVS giua node i va j, dieu khien boi dien ap giua node k va l
    def __init__(self, name, np, nm, ncp, ncm, value):
        self.name = name
        self.n_p = np
        self.n_m = nm
        self.nc_p = ncp
        self.nc_m = ncm
        self.A = value # Voltage gain


    # Mo hinh DC
    def stamp_dc(self, G, b, ctx):
        if self.name not in ctx.vs_index:
            raise ValueError(f"{self.name}: VCVS not indexed")

        # Ma tran dan anp G
        k = ctx.vs_index[self.name]

        if self.n_p != None:
            G[self.n_p][k] += 1
            G[k][self.n_p] += 1

        if self.n_m != None:
            G[self.n_m][k] -= 1
            G[k][self.n_m] -= 1

        if self.nc_p != None:
            G[k][self.nc_p] -= self.A

        if self.nc_m != None:
            G[k][self.nc_m] += self.A

    

    # Hien thi thong tin linh kien (cho debug)
    def __repr__(self):
        return f"VCVS({self.name}, {self.n_p}, {self.n_m}, {self.nc_p}, {self.nc_m}, {self.A}) at {hex(id(self))}"