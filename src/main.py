# main.py

from parser.netlist_parser import parse_netlist
from mna_builder.mna_builder import MNABuilder
from solver.solver import Solver
from analysis.ac_analysis import ACAnalysis
from analysis.plot import plot_bode


def main():
    # Parse circuit tu netlist
    circuit = parse_netlist("netlist.cir")

    # Print node map
    print("=== NODE MAP ===")
    for name, idx in circuit.node_map.items():
        print(f"{name} -> {idx}")

    # Print component list
    print("\n=== COMPONENTS ===")
    for comp in circuit.components:
        print(comp)

    print("\n=== Analysis===")
    # Build va solve mach
    builder = MNABuilder(circuit)
    solver = Solver()
    analysis = circuit.circuit_analysis

    if analysis and analysis["type"] == "ac":
        print(">>> RUN AC ANALYSIS")

        ac = ACAnalysis(circuit, builder, solver)
        results = ac.run()

        # In ket qua
        print(">>> DONE, number of points:", len(results))
        for f, x in results:
            print(f"f = {f:.2f} Hz, x = {x}")

        # Ve do thi bode
        print(">>> Bode plot")
        plot_bode(results, vin_idx=0, vout_idx=1, title="Bode plot")





if __name__ == "__main__":
    main()
