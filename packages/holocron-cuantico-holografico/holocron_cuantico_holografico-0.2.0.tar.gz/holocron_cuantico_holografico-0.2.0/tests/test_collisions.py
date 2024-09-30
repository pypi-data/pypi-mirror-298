import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import unittest
from src.holobit import Holobit
from src.collisions import Collisions


class TestCollisions(unittest.TestCase):

    def test_collision_success(self):
        """Test de colisión exitosa entre holobits con spins opuestos."""
        holobit1 = Holobit(spin=0.5)
        holobit2 = Holobit(spin=-0.5)

        new_holobit = Collisions.collide(holobit1, holobit2)

        self.assertIsNotNone(new_holobit)
        # Verificamos que el spin de la nueva partícula sea 0.5 o -0.5
        self.assertIn(new_holobit.spin, [0.5, -0.5])
        self.assertTrue(isinstance(new_holobit, Holobit))
        self.assertEqual(len(new_holobit.position), 3)

    def test_collision_failure(self):
        """Test de colisión fallida entre holobits con spins iguales."""
        holobit1 = Holobit(spin=0.5)
        holobit2 = Holobit(spin=0.5)

        new_holobit = Collisions.collide(holobit1, holobit2)

        self.assertIsNone(new_holobit)


if __name__ == '__main__':
    unittest.main()
