# holobit.py
import numpy as np
from scipy.constants import golden


class Holobit:
    def __init__(self, position=None, spin=None, dimension=0):
        self.position = position if position is not None else np.random.randn(3) * golden ** dimension
        self.spin = spin if spin is not None else np.random.choice([-0.5, 0.5])
        self.dimension = dimension  # La dimensión fractal en la que reside
        self.entangled_with = None  # Permite establecer entrelazamiento con otros holobits

    def entangle(self, other_holobit):
        """Entrelazar este holobit con otro holobit"""
        if self.spin == other_holobit.spin:
            other_holobit.spin = -self.spin
            self.entangled_with = other_holobit
            print(f"Entrelazamiento creado: Spin 1: {self.spin}, Spin 2: {other_holobit.spin}")
        else:
            print(f"Ya están entrelazados: Spin 1: {self.spin}, Spin 2: {other_holobit.spin}")

    def apply_rotation(self, angle):
        """Aplicar una rotación cuántica al spin"""
        self.spin = self.spin * np.cos(angle)
        print(f"Rotación aplicada: Nuevo spin = {self.spin}")

    def collide(self, other_holobit):
        """Simular una colisión cuántica entre dos holobits"""
        if self.spin == -other_holobit.spin:
            new_holobit = Holobit(position=(self.position + other_holobit.position) / 2, dimension=self.dimension)
            print(f"Colisión exitosa: Nueva partícula en posición {new_holobit.position} con spin {new_holobit.spin}")
            return new_holobit
        else:
            print("Colisión fallida, los spins no son opuestos.")
            return None
