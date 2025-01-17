import random
import numpy as np
from dataclasses import dataclass
import matplotlib.pyplot as plt

PARTICLE_NO = 40
POSITION_RANGE = (-10, 10)  # we asume the range has a form of an N dimensional cube
VELOCITY_RANGE = (-1, 1)
EPOCHS = 101
DIMENSIONS = 2
DESCENDING = True

parameter_sets = [
    {'W': 0.4, 'C1': 1.3, 'C2': 1.4, 'label': 'SET A'},
    {'W': 0.6, 'C1': 1.7, 'C2': 1.8, 'label': 'SET B'},
    {'W': 0.8, 'C1': 2.0, 'C2': 2.1, 'label': 'SET C'}
]

@dataclass
class Particle:
    position: np.ndarray
    velocity: float
    best_position: np.ndarray
    best_value: np.float64

    def __init__(self):
        self.position = np.array([random.uniform(*POSITION_RANGE) for _ in range(DIMENSIONS)])
        self.velocity = random.uniform(*VELOCITY_RANGE)
        self.best_position = self.position
        self.best_value = function_(self.position)


def main():
    random.seed(0)

    for param_set in parameter_sets:

        velocity, particles, global_best_value, global_best_position = init_vars()
        
        w = param_set['W']
        c1 = param_set['C1']
        c2 = param_set['C2']
        set_label = param_set['label']

        contour_plot(particles, f"Inicio {set_label}")

        for epoch_no in range(EPOCHS):
            # TODO: revisar esto
            for particle in particles:
                particle.velocity = get_next_velocity(velocity, global_best_value, particle, w, c1, c2)
                particle.position = next_position(particle.position, particle.velocity)
                position_value_z = function_(particle.position)

                if (DESCENDING and position_value_z < particle.best_value) or (
                        not DESCENDING and position_value_z > particle.best_value):
                    particle.best_position = particle.position
                    particle.best_value = position_value_z

                if (DESCENDING and position_value_z < global_best_value) or (
                        not DESCENDING and position_value_z > global_best_value):
                    global_best_value = position_value_z
                    global_best_position = particle.position

            if epoch_no == EPOCHS // 2:
                contour_plot(particles, f"Mitad {set_label}")
            if epoch_no == EPOCHS - 1:
                contour_plot(particles, f"Final {set_label}")

        print(f"Set: {set_label}")
        print(f"Best value: {global_best_value}")
        print(f"Best position: {global_best_position}")






def init_vars():
    velocity = random.uniform(-1, 1)
    particles = [Particle() for _ in range(PARTICLE_NO)]
    global_best = max(particles, key=lambda p: function_(p.best_position))
    return velocity, particles, global_best.best_value, global_best.best_position


def function_(vector: np.ndarray) -> np.float64:
    x = vector[0]
    y = vector[1]
    return np.float64((x - 3) ** 2 + (y - 2) ** 2)


def get_next_velocity(velocity, global_best, particle: Particle, W, C1, C2):
    inertia = W * velocity
    cognitive = C1 * random.random() * (particle.best_position - particle.position)
    social = C2 * random.random() * (global_best - particle.position)
    return inertia + cognitive + social


def next_position(position, velocity):
    return position + velocity


def contour_plot(particles, title=""):
    particle_pos = [particle.position for particle in particles]


    # Unzip the list of tuples into two lists: x and y
    x_, y_ = zip(*particle_pos)
    max_y = max(y_)
    min_y = min(y_)
    max_x = max(x_)
    min_x = min(x_)

    # Create a mesh grid for the contour plot
    x = np.linspace(min_x, max_x, 100)
    y = np.linspace(min_y, max_y, 100)
    X, Y = np.meshgrid(x, y)
    param = (X, Y)
    Z = function_(param)

    # Specify the number of levels or an array of custom levels
    num_levels = 20  # For example, 20 levels
    levels = np.linspace(Z.min(), Z.max(), num_levels)

    # Plot the contour plot and scatter plot on the same figure
    plt.figure()
    cp = plt.contour(X, Y, Z, levels=levels)
    plt.clabel(cp, inline=True, fontsize=10)
    plt.scatter(x_, y_, color='red')  # Optional: Customize scatter plot appearance
    plt.title(f"Curvas de Nivel con Scatter Plot - {title}")
    plt.xlabel('x')
    plt.ylabel('y')

    # Save the figure as a PNG file
    plt.savefig(f"out/{title}.png")
    plt.show()



if __name__ == "__main__":
    main()
