# components/vccs.py
# Voltage-Controlled Current Source (VCCS)

from components.base import Component

class VCCS(Component):
    # Khai bao VCCS giua node i va j, dieu khien boi dien ap giua node k va l
    def __init__(self, name, np, nm, ncp, ncm, value):
        self.name = name
        self.n_p = np
        self.n_m = nm
        self.nc_p = ncp
        self.nc_m = ncm
        self.Gm = value  # Transconductance (S)


    # Mo hinh DC
    def stamp_dc(self, G, b, ctx):
        # Ma tran dan nap G
        if self.n_p != None and self.nc_p != None:
            G[self.n_p][self.nc_p] += self.Gm

        if self.n_p != None and self.nc_m != None:
            G[self.n_p][self.nc_m] -= self.Gm

        if self.n_m != None and self.nc_p != None:
            G[self.n_m][self.nc_p] -= self.Gm

        if self.n_m != None and self.nc_m != None:
            G[self.n_m][self.nc_m] += self.Gm

    

    # Hien thi thong tin linh kien (cho debug)
    def __repr__(self):
        return f"VCCS({self.name}, {self.n_p}, {self.n_m}, {self.nc_p}, {self.nc_m}, {self.Gm}) at {hex(id(self))}"