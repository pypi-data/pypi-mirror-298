# interactions.py
import numpy as np
from scipy.constants import golden


class Interactions:
    def __init__(self, k_0=1.0, lambda_spin=0.5):
        self.k_0 = k_0
        self.lambda_spin = lambda_spin

    def confinement_force(self, holobit1, holobit2):
        r = np.linalg.norm(holobit1.position - holobit2.position)
        k_d = self.k_0 * golden**holobit1.dimension
        return k_d * r

    def spin_interaction(self, holobit1, holobit2):
        return self.lambda_spin * (holobit1.spin * holobit2.spin)
