# entanglement.py

class Entanglement:
    @staticmethod
    def entangle(holobit1, holobit2):
        """
        Realiza el entrelazamiento cuántico entre dos holobits.
        Si los spins de ambos holobits son iguales, se invierte el spin del segundo holobit,
        creando un estado de entrelazamiento cuántico.
        """
        if holobit1.spin == holobit2.spin:
            holobit2.spin = -holobit1.spin
            print(f"Entrelazamiento creado: Spin 1: {holobit1.spin}, Spin 2: {holobit2.spin}")
        else:
            print(f"Ya están entrelazados: Spin 1: {holobit1.spin}, Spin 2: {holobit2.spin}")
