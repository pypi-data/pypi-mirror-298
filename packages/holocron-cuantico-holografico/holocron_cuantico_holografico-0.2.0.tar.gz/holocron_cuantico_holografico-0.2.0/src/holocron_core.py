# holocron_core.py
from src.holobit import Holobit


class Holocron:
    def __init__(self, num_holobits=360, num_families=12):
        self.num_holobits = num_holobits
        self.num_families = num_families
        self.holocron = {'holobits': []}
        self.create_holobits()

    def create_holobit_family(self, dimension, num_holobits):
        family = []
        for i in range(num_holobits):
            holobit = Holobit(dimension=dimension)
            family.append(holobit)
        return family

    def create_holobits(self):
        for dimension in range(1, 16):  # Vamos hasta 15 dimensiones
            holobit_family = self.create_holobit_family(dimension, self.num_families)
            self.holocron['holobits'].append(holobit_family)

    def get_family(self, dimension):
        return self.holocron['holobits'][dimension]

    def visualize_family(self, family, title="Holobit Family"):
        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for holobit in family:
            position = holobit.position
            ax.scatter(position[0], position[1], position[2], s=100)
            ax.text(position[0], position[1], position[2], f"Spin: {holobit.spin}", fontsize=12)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(title)
        plt.show()
