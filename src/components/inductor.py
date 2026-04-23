# components/inductor.py

import numpy as np
from components.base import Component

class Inductor(Component):
    # Khai bao cuon cao L giua node i va j
    def __init__(self, name, node_i, node_j, value):
        self.name = name
        self.i = node_i
        self.j = node_j
        self.L = value


    # Mo hinh DC (cuon cam xem nhu short circuit)
    def stamp_dc(self, G, b, ctx):
        if self.name not in ctx.vs_index:
            raise ValueError(f"{self.name}: Inductor not indexed")

        k = ctx.vs_index[self.name]

        if self.i != None:
            G[self.i][k] += 1
            G[k][self.i] += 1

        if self.j != None:
            G[self.j][k] -= 1
            G[k][self.j] -= 1


    # Mo hinh AC
    def stamp_ac(self, G, b, ctx):
        Zl = 1 / (1j * ctx.omega * self.L)

        if self.i is not None:
            G[self.i, self.i] += Zl

        if self.j is not None:
            G[self.j, self.j] += Zl

        if self.i is not None and self.j is not None:
            G[self.i, self.j] -= Zl
            G[self.j, self.i] -= Zl

    
    # Hien thi thong tin linh kien (cho debug)
    def __repr__(self):
        return f"Inductor({self.name}, {self.i}, {self.j}, {self.L}) at {hex(id(self))}"