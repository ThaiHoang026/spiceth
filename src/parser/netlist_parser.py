# parser/netlist_parser.py

# Doc linh kien tu netlist va tao object Circuit
# Tao danh sach linh kien va index node

from components.resistor import Resistor
from components.current_source import CurrentSource
from components.voltage_source import VoltageSource
from components.capacitor import Capacitor
from components.inductor import Inductor
from components.vccs import VCCS
from components.vcvs import VCVS
from components.cccs import CCCS
from components.ccvs import CCVS


component_map = {
    'R': Resistor,
    'I': CurrentSource,
    'V': VoltageSource,
    'C': Capacitor,
    'L': Inductor,
    'G': VCCS,
    'E': VCVS,
    'F': CCCS,
    'H': CCVS
}

class Circuit:
    # khoi tao Circuit
    def __init__(self):
        self.node_map = {}   # node_name : node_index
        self.components = [] # Resistor, CurrentSource, ...
        self.circuit_analysis = {}
        self.next_node_index = 0


    # Lay, tao index cua node trong map_node
    def get_node_index(self, node_name):
        if node_name == "0": # ground node
            return None
        
        elif node_name not in self.node_map:
            self.node_map[node_name] = self.next_node_index
            self.next_node_index += 1

        return self.node_map[node_name]
    

    # Them component vao circuit
    def add_component(self, comp):
        self.components.append(comp)


# Tinh gia tri cua component co tien to (1k, 20u, ...)
def parse_value(value_str):
    multipliers = {
        't'  : 1e12,
        'g'  : 1e9,
        'meg': 1e6,
        'k'  : 1e3,
        'm'  : 1e-3,
        'u'  : 1e-6,
        'n'  : 1e-9,
        'p'  : 1e-12,
    }

    # Gia tri co tien to
    value_str = value_str.lower()

    for key in sorted(multipliers.keys(), key = len, reverse = True): # sort theo do dai key de xu ly tien to "meg" truoc "g"
        if value_str.endswith(key):
            number_part = value_str[:-len(key)]
            return float(number_part) * multipliers[key]
        
    # Gia tri khong co tien to
    return float(value_str)


def is_number(s):
    try:
        float(s)
        return True
    except:
        return False


# Ham parse netlist
def parse_netlist(file_name):
    circuit = Circuit()

    with open(file_name, 'r') as f:
        used_names = set() # Set de kiem tra ten linh kien trung lap

        for line in f:

            line = line.strip() # Xoa khoang trong o dau va cuoi dong
            if not line or line.startswith('*'): # Bo qua dong trong va comment
                continue
            
            # Tach dong thanh tokens
            tokens = line.split()
            
            # Kiem tra linh kien trung ten
            name = tokens[0]
            if name in used_names:
                raise ValueError(f"Duplicate component name: {name}")
            used_names.add(name)

            # Xac dinh loai linh kien va tao object
            prefix = name[0].upper()
            # Neu linh kien hop le va co trong component_map
            if prefix in component_map: 
                # Linh kien thu dong: name node1 node2 value
                if prefix in ['R', 'C', 'L']:
                    _, node1, node2, value_str = tokens

                    i = circuit.get_node_index(node1)
                    j = circuit.get_node_index(node2)

                    value = parse_value(value_str)

                    comp_class = component_map[prefix]
                    comp = comp_class(name, i, j, value)

                    circuit.add_component(comp)

                # Linh kien nguon doc lap
                elif prefix in ['I', 'V']:

                    dc_value = None
                    ac_mag = None
                    ac_phase = 0

                    # name n1 n2 dc_value
                    if len(tokens) == 4:
                        _, node1, node2, value_str = tokens
                        dc_value = parse_value(value_str)

                    # Gom nhieu loai nguon
                    elif len(tokens) >= 5:
                        _, node1, node2 = tokens[:3]

                        idx = 3
                        while idx < len(tokens):
                            token = tokens[idx].lower()

                            # Gia tri DC
                            if token == "dc":
                                if idx + 1 >= len(tokens) or not is_number(tokens[idx + 1]):
                                    raise ValueError(f"{name} invalid DC value")
                                dc_value = parse_value(tokens[idx + 1])
                                idx += 2

                            # Gia tri AC
                            elif token == "ac":
                                if idx + 1 >= len(tokens) or not is_number(tokens[idx + 1]):
                                    raise ValueError(f"{name} invalid AC magnitude")
                                ac_mag = parse_value(tokens[idx + 1])

                                if idx + 2 < len(tokens) and is_number(tokens[idx + 2]):
                                    ac_phase = parse_value(tokens[idx + 2])
                                    idx += 3
                                else:
                                    idx += 2

                            # Loi type
                            else:
                                raise ValueError(f"{name} unknown token: {token}")

                    # Loi syntax
                    else:
                        raise ValueError(f"Invalid format for source: {line}")

                    # Them linh kien vao circuit
                    i = circuit.get_node_index(node1)
                    j = circuit.get_node_index(node2)

                    ac = None if ac_mag is None else (ac_mag, ac_phase)

                    comp_class = component_map[prefix]
                    comp = comp_class(name, i, j, dc_value, ac=ac, transient=None)

                    circuit.add_component(comp)                    


                # Linh kien dieu kien bang dien ap (VCCS, VCVS)
                # name np nm ncp ncm gain
                elif prefix in ['G', 'E']:
                    _, np, nm, ncp, ncm, gain_str = tokens

                    np = circuit.get_node_index(np)
                    nm = circuit.get_node_index(nm)
                    ncp = circuit.get_node_index(ncp)
                    ncm = circuit.get_node_index(ncm)

                    gain = parse_value(gain_str)

                    comp_class = component_map[prefix]
                    comp = comp_class(name, np, nm, ncp, ncm, gain)

                    circuit.add_component(comp)

                # Linh kien dieu kien bang dong dien (CCCS, CCVS)
                # name np nm vxxx gain
                elif prefix in ['F', 'H']:
                    _, np, nm, vxxx, gain_str = tokens

                    np = circuit.get_node_index(np)
                    nm = circuit.get_node_index(nm)

                    gain = parse_value(gain_str)

                    comp_class = component_map[prefix]
                    comp = comp_class(name, np, nm, vxxx, gain)

                    circuit.add_component(comp)

            # Khong xac dinh duoc loai linh kien
            else:
                raise ValueError(f"Unknown component: {name}")

            
    return circuit