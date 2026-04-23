# main.py

from parser.netlist_parser import parse_netlist
from mna_builder.mna_builder import MNABuilder
from solver.solver import Solver


def main():
    # Parse circuit tu netlist
    circuit = parse_netlist("netlist.cir")

    # Print node map
    print("=== NODE MAP ===")
    for name, idx in circuit.node_map.items():
        print(f"{name} -> {idx}")

    # Print list cac components
    print("\n=== COMPONENTS ===")
    for comp in circuit.components:
        print(comp)

    # Build, print ma tran MNA
    print("\n=== MATRIX ===")
    G, b = MNABuilder(circuit).build_ac()
     
    # Giai phuong trinh MNA
    x = Solver().solve_linear(G, b)

    # Print vector x da giai
    print("\n=== SOLUTION ===")
    print("X =\n", x)

    # Print dien ap node
    print("\n=== VOLTAGES ===")
    for node_name, node_idx in circuit.node_map.items():
        if node_name == '0':
            print(f"V({node_name}) = 0.000000 V")
        else:
            print(f"V({node_name}) = {x[node_idx]:.6f} V")



if __name__ == "__main__":
    main()
