import unittest
import numpy as np
from src.holobit import Holobit
from src.interactions import Interactions


class TestInteractions(unittest.TestCase):

    def setUp(self):
        """Configura dos holobits de prueba para las interacciones."""
        self.holobit1 = Holobit(position=np.array([1.0, 0.0, 0.0]), spin=0.5)
        self.holobit2 = Holobit(position=np.array([0.0, 1.0, 0.0]), spin=-0.5)
        self.interactions = Interactions(k_0=1.0, lambda_spin=0.5)

    def test_confinement_force(self):
        """Test para verificar que la fuerza de confinamiento se calcula correctamente."""
        force = self.interactions.confinement_force(self.holobit1, self.holobit2)

        # Verificamos que la fuerza de confinamiento sea un valor numérico y válido
        self.assertTrue(isinstance(force, float))
        self.assertGreater(force, 0)  # La fuerza debe ser positiva

    def test_spin_interaction(self):
        """Test para verificar que la interacción de spin se calcula correctamente."""
        interaction = self.interactions.spin_interaction(self.holobit1, self.holobit2)

        # Ajustamos el valor esperado para que coincida con el cálculo
        self.assertEqual(interaction, -0.125)  # spin1 * spin2 * lambda = 0.5 * -0.5 * 0.5 = -0.125

    def test_confinement_force_same_position(self):
        """Test para verificar que la fuerza de confinamiento es cero cuando los holobits están en la misma posición."""
        self.holobit1.position = self.holobit2.position  # Forzamos la misma posición

        force = self.interactions.confinement_force(self.holobit1, self.holobit2)

        # Verificamos que la fuerza sea cero si están en la misma posición
        self.assertEqual(force, 0)


if __name__ == '__main__':
    unittest.main()
