# components/current_source.py

from components.base import Component

class CurrentSource(Component):
    # Khai bao nguon dong I giua node i va j
    def __init__(self, name, node_i, node_j,
                 dc_value=None,
                 ac=None,
                 transient=None):
        
        self.name = name
        self.i = node_i
        self.j = node_j
        
        self.dc = dc_value
        self.ac = ac
        self.transient = transient


    # Mo hinh DC
    def stamp_dc(self, G, b, ctx):
        # Vector nguon input
        if self.i != None:
            b[self.i] -= self.dc
        if self.j != None:
            b[self.j] += self.dc



    # Hien thi thong tin linh kien (cho debug)
    def __repr__(self):
        return f"CurrentSource({self.name}, {self.i}, {self.j}, {self.dc}) at {hex(id(self))}"