import numpy as np

class ACAnalysis:
    def __init__(self, circuit, builder, solver):
        self.circuit = circuit
        self.builder = builder
        self.solver = solver

    
    # Tao cac diem tinh tren thang tan so
    def generate_frequencies(self, analysis):
        sweep = analysis["sweep"]
        points = analysis["points"]
        f_start = analysis["f_start"]
        f_end = analysis["f_end"]

        # Decade
        if sweep == "DEC":
            decades = np.log10(f_end) - np.log10(f_start)
            num_points = int(points * decades) + 1
            return np.logspace(np.log10(f_start), np.log10(f_end), num_points)
        
        # Linear
        elif sweep == "LIN":
            return np.linspace(f_start, f_end, points)
    

        elif sweep == "OCT":
            octaves = np.log2(f_end / f_start)
            num_points = int(points * octaves) + 1
            return np.logspace(np.log10(f_start), np.log10(f_end), num_points)
        
        else:
            raise ValueError("Unkown sweep type")
        

    def run(self):
        analysis = self.circuit.circuit_analysis
        freqs = self.generate_frequencies(analysis)

        results = []

        for f in freqs:
            omega = 2 * np.pi * f

            G, b = self.builder.build_ac(omega)
            x = self.solver.solve_linear(G, b)

            results.append((f, x))

        return results
