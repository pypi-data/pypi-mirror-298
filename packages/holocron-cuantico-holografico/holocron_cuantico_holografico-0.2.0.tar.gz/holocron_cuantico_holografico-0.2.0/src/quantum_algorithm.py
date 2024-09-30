# quantum_algorithm.py


class QuantumAlgorithm:
    def __init__(self, interactions):
        self.interactions = interactions

    def run_algorithm(self, family):
        # Entrelazar los holobits y aplicar colisiones
        for i in range(len(family)):
            holobit1 = family[i]
            for j in range(i + 1, len(family)):
                holobit2 = family[j]
                holobit1.entangle(holobit2)
                holobit1.collide(holobit2)

        print("Algoritmo cuántico ejecutado con éxito")
