import unittest
from src.holocron_core import Holocron
from src.holobit import Holobit


class TestHolocronCore(unittest.TestCase):

    def test_holocron_creation(self):
        """Test para verificar que el Holocron se crea correctamente con la cantidad de holobits especificada."""
        holocron = Holocron(num_holobits=360, num_families=12)

        # Verificamos que el Holocron tenga las familias correctas
        self.assertEqual(len(holocron.holocron['holobits']), 15)  # Hasta 15 dimensiones
        self.assertEqual(len(holocron.holocron['holobits'][0]), 12)  # 12 holobits en la primera dimensión

    def test_get_family(self):
        """Test para verificar que se puede obtener correctamente una familia de holobits por dimensión."""
        holocron = Holocron(num_holobits=360, num_families=12)
        family = holocron.get_family(5)

        # Verificamos que la familia obtenida sea correcta
        self.assertEqual(len(family), 12)  # La familia debe tener 12 holobits
        self.assertTrue(isinstance(family[0], Holobit))  # Cada miembro de la familia debe ser un Holobit

    def test_holocron_visualization(self):
        """Test para verificar que el Holocron puede visualizar correctamente una familia de holobits."""
        holocron = Holocron(num_holobits=360, num_families=12)
        family = holocron.get_family(1)

        try:
            holocron.visualize_family(family, title="Test Visualization")
            success = True
        except Exception as e:
            success = False
            print(f"Error en la visualización: {e}")

        self.assertTrue(success)


if __name__ == '__main__':
    unittest.main()
