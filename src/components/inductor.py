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
        # Ma tran dan nap G
        mat_len = G.shape[0]
        G = np.pad(G, ((0,1),(0,1)))
        

        if self.i != None:
            G[self.i][mat_len] += 1
            G[mat_len][self.i] += 1

        if self.j != None:
            G[self.j][mat_len] -= 1
            G[mat_len][self.j] -= 1


    
    # Hien thi thong tin linh kien (cho debug)
    def __repr__(self):
        return f"Inductor({self.name}, {self.i}, {self.j}, {self.L}) at {hex(id(self))}"