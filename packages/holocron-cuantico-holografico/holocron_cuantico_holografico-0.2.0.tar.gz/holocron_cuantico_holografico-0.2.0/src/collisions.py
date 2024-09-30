import numpy as np
from src.holobit import Holobit


class Collisions:
    @staticmethod
    def collide(p1, p2):
        """
        Simula una colisión cuántica entre dos holobits.
        Si los spins son opuestos, genera un nuevo holobit con un spin basado en uno de los holobits originales.
        """
        if p1.spin == -p2.spin:
            # Si los spins son opuestos, creamos una nueva partícula con la posición media
            new_position = (p1.position + p2.position) / 2
            # Generamos un nuevo holobit con un spin aleatorio o basado en uno de los holobits
            new_spin = np.random.choice([0.5, -0.5])  # Puedes cambiar esta lógica si lo deseas
            new_holobit = Holobit(position=new_position, spin=new_spin, dimension=p1.dimension)
            print(f"Aniquilación: Nueva partícula en posición {new_holobit.position} con spin {new_holobit.spin}")
            return new_holobit
        else:
            print("No hay aniquilación, los spins no son opuestos.")
            return None
