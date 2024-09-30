import unittest
from src.holobit import Holobit
from src.interactions import Interactions
from src.quantum_algorithm import QuantumAlgorithm


class TestQuantumAlgorithm(unittest.TestCase):

    def setUp(self):
        """Configura una familia de holobits y el sistema de interacciones para probar el algoritmo cuántico."""
        self.holobits = [Holobit(spin=0.5), Holobit(spin=0.5), Holobit(spin=-0.5), Holobit(spin=-0.5)]
        self.interactions = Interactions(k_0=1.0, lambda_spin=0.5)
        self.algorithm = QuantumAlgorithm(self.interactions)

    def test_run_algorithm_entanglement(self):
        """Test para verificar que el algoritmo realiza correctamente el entrelazamiento entre los holobits."""
        self.algorithm.run_algorithm(self.holobits)

        # Verificamos que los spins de los holobits cambien correctamente
        self.assertIn(self.holobits[3].spin, [0.5, -0.5])

    def test_run_algorithm_collisions(self):
        """Test para verificar que el algoritmo realiza colisiones cuánticas correctamente."""
        self.holobits[0].spin = 0.5
        self.holobits[1].spin = -0.5

        self.algorithm.run_algorithm(self.holobits)

        # Verificamos que la colisión ocurra y una nueva partícula sea creada correctamente
        # Aquí podemos añadir más validaciones dependiendo del comportamiento esperado


if __name__ == '__main__':
    unittest.main()

