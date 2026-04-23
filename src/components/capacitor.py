# components/capacitor.py

from components.base import Component

class Capacitor(Component):
    # Khai bao tu dien C giua node i va j
    def __init__(self, name, node_i, node_j, value):
        self.name = name
        self.i = node_i
        self.j = node_j
        self.C = value

    
    # Mo hinh DC
    def stamp_dc(self, G, b, ctx):
        # Trong mo hinh DC, tu dien xem nhu mach ho
        pass

    
    # Mo hinh AC
    def stamp_ac(self, G, b, ctx):
        Zc = 1j * ctx.omega * self.C
        if self.i is not None:
            G[self.i, self.i] += Zc

        if self.j is not None:
            G[self.j, self.j] += Zc

        if self.i is not None and self.j is not None:
            G[self.i, self.j] -= Zc
            G[self.j, self.i] -= Zc
    

    def __repr__(self):
        return f"Capacitor({self.name}, {self.i}, {self.j}, {self.C}) at {hex(id(self))}"