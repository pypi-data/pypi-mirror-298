import unittest
from src.holobit import Holobit
from src.entanglement import Entanglement


class TestEntanglement(unittest.TestCase):

    def test_entanglement_creation(self):
        """Test de entrelazamiento exitoso entre holobits con spins iguales."""
        holobit1 = Holobit(spin=0.5)
        holobit2 = Holobit(spin=0.5)

        # Realizamos el entrelazamiento
        Entanglement.entangle(holobit1, holobit2)

        # Verificamos que el segundo holobit haya cambiado su spin a -0.5
        self.assertEqual(holobit1.spin, 0.5)
        self.assertEqual(holobit2.spin, -0.5)

    def test_already_entangled(self):
        """Test para verificar que los holobits ya están entrelazados si sus spins son opuestos."""
        holobit1 = Holobit(spin=0.5)
        holobit2 = Holobit(spin=-0.5)

        # Intentamos entrelazarlos
        Entanglement.entangle(holobit1, holobit2)

        # Verificamos que no haya cambiado nada porque ya estaban entrelazados
        self.assertEqual(holobit1.spin, 0.5)
        self.assertEqual(holobit2.spin, -0.5)


if __name__ == '__main__':
    unittest.main()
