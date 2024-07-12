import random
import numpy as np
from dataclasses import dataclass

PARTICLE_NO = 40
POSITION_RANGE = (-10, 10)  # we asume the range has a form of an N dimensional cube
VELOCITY_RANGE = (-1, 1)
W = 0.5
C1 = 1.5
C2 = 1.5
EPOCHS = 100
DIMENSIONS = 3


@dataclass
class Particle:
    position: np.ndarray
    velocity: float
    best_position: np.ndarray
    best_value: float

    def __init__(self):
        self.position = np.array([random.uniform(*POSITION_RANGE) for _ in range(DIMENSIONS)])
        self.velocity = random.uniform(*VELOCITY_RANGE)
        self.best_position = self.position
        self.best_value = function(self.position, self.position)


def main():
    random.seed(0)
    velocity, particles, global_best = init_vars()

    for _ in range(EPOCHS):
        # TODO: revisar esto
        for particle in particles:
            particle.velocity = get_next_velocity(velocity, global_best, particle)
            particle.position = next_position(particle.position, particle.velocity)
            value = function(*particle.position)
            if value < particle.best_value:
                particle.best_value = value
                particle.best_position = particle.position
            if value < global_best.best_value:
                global_best = particle


def init_vars():
    velocity = random.uniform(-1, 1)
    particles = [Particle() for _ in range(PARTICLE_NO)]
    global_best = max(particles, key=lambda p: p.best_position[-1])
    return velocity, particles, global_best


def function(x, y):
    return (x - 3) ** 2 + (y - 2) ** 2


def get_next_velocity(velocity, global_best, particle: Particle):
    inertia = W * velocity
    cognitive = C1 * random.random() * (particle.best_position - particle.position)
    social = C2 * random.random() * (global_best - particle.position)
    return inertia + cognitive + social


def next_position(position, velocity):
    return position + velocity


if __name__ == "__main__":
    main()
