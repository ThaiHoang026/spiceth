# components/current_source.py

from components.base import Component

class CurrentSource(Component):
    # Khai bao nguon dong I giua node i va j
    def __init__(self, name, node_i, node_j,
                dc_value=None,
                ac_value=None,
                transient=None):
        
        self.name = name
        self.i = node_i
        self.j = node_j
        
        self.dc = dc_value
        self.ac = ac_value
        self.tran = transient


    # Mo hinh phan tu linear current
    def _stamp_linear(self, b, I):
        if self.i != None:
            b[self.i] -= I
        if self.j != None:
            b[self.j] += I

    
    # Mo hinh DC
    def stamp_dc(self, G, b, ctx):
        self._stamp_linear(b, self.dc)

    
    # Mo hinh AC
    def stamp_ac(self, G, b, ctx):
        self._stamp_linear(b, self.ac)



    # Hien thi thong tin linh kien (cho debug)
    def __repr__(self):
        return f"CurrentSource({self.name}, {self.i}, {self.j}, {self.dc}, {self.ac}, {self.tran}) at {hex(id(self))}"