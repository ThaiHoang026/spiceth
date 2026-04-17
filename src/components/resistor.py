# components/resistor.py

from components.base import Component

class Resistor(Component):
    # Khai bao dien tro R giua node i va j
    def __init__(self, name, node_i, node_j, value):
        self.name = name
        self.i = node_i
        self.j = node_j
        self.R = value



    # Mo hinh ma tran dan nap G
    def stamp_dc(self, G, b, ctx):
        g = 1 / self.R

        if self.i is not None:
            G[self.i, self.i] += g

        if self.j is not None:
            G[self.j, self.j] += g

        if self.i is not None and self.j is not None:
            G[self.i, self.j] -= g
            G[self.j, self.i] -= g

        

    # Hien thi thong tin linh kien (cho debug)
    def __repr__(self):
        return f"Resistor({self.name}, {self.i}, {self.j}, {self.R}) at {hex(id(self))}"
