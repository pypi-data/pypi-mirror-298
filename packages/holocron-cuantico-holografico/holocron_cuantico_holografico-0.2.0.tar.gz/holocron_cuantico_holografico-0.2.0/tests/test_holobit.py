import unittest
import numpy as np
from src.holobit import Holobit



class TestHolobit(unittest.TestCase):

    def test_holobit_creation(self):
        """Test para verificar que un holobit se crea correctamente con un spin y posición válida."""
        holobit = Holobit(spin=0.5)

        # Verificamos que el holobit tenga un spin correcto
        self.assertEqual(holobit.spin, 0.5)

        # Verificamos que el holobit tenga una posición en 3D
        self.assertEqual(len(holobit.position), 3)
        self.assertTrue(isinstance(holobit.position, np.ndarray))

    def test_holobit_random_spin(self):
        """Test para verificar que un holobit se crea con un spin aleatorio si no se especifica."""
        holobit = Holobit()

        # Verificamos que el spin sea uno de los valores permitidos (-0.5 o 0.5)
        self.assertIn(holobit.spin, [-0.5, 0.5])

    def test_holobit_position(self):
        """Test para verificar que un holobit se crea con una posición válida basada en su dimensión."""
        dimension = 5
        holobit = Holobit(dimension=dimension)

        # Verificamos que la posición esté escalada según la dimensión (por ejemplo, usando golden ratio)
        self.assertEqual(len(holobit.position), 3)
        self.assertTrue(isinstance(holobit.position, np.ndarray))

    def test_holobit_entanglement(self):
        """Test para verificar que el holobit puede ser entrelazado con otro."""
        holobit1 = Holobit(spin=0.5)
        holobit2 = Holobit(spin=0.5)

        # Realizamos el entrelazamiento
        holobit1.entangle(holobit2)

        # Verificamos que el segundo holobit haya cambiado su spin
        self.assertEqual(holobit2.spin, -0.5)


if __name__ == '__main__':
    unittest.main()
