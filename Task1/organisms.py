"""concrete organisms: Plant (grass), Sheep (herbivore), Wolf (predator)."""

import random
from base import Animal, Organism


class Plant(Organism):
    """stationary; regrowth is driven by Ecosystem, not the plant itself."""

    def __init__(self, x, y, energy=10):
        super().__init__(x, y, energy)

    def color(self):  return "#2D6A4F"
    def symbol(self): return "G"

    def update(self, eco):
        return None


class Sheep(Animal):
    """herbivore: seeks grass, reproduces when well-fed."""

    def __init__(self, x, y, energy=20, repr_threshold=40, grass_energy=10):
        super().__init__(x, y, energy, repr_threshold)
        self.grass_energy = grass_energy

    def color(self):  return "#E8E8D0"
    def symbol(self): return "S"

    def _act(self, eco):
        nbrs = eco.grid.neighbors(self.x, self.y)
        # prefer grass cells with no occupant
        targets = [
            c for c in nbrs
            if eco.grid.has_grass(*c) and eco.grid.animal_at(*c) is None
        ]
        if not targets:
            targets = [c for c in nbrs if eco.grid.animal_at(*c) is None]

        if targets:
            nx, ny = random.choice(targets)
            eco.grid.move_animal(self, nx, ny)
            if eco.grid.has_grass(nx, ny):
                eco.grid.remove_grass(nx, ny)
                self.energy += self.grass_energy

        if self.energy >= self.repr_threshold:
            self.energy //= 2
            spawn = [c for c in eco.grid.neighbors(self.x, self.y)
                     if eco.grid.animal_at(*c) is None]
            if spawn:
                bx, by = random.choice(spawn)
                return Sheep(bx, by, self.energy, self.repr_threshold, self.grass_energy)
        return None


class Wolf(Animal):
    """predator: hunts sheep, starves without prey."""

    def __init__(self, x, y, energy=30, repr_threshold=60, sheep_energy=25):
        super().__init__(x, y, energy, repr_threshold)
        self.sheep_energy = sheep_energy

    def color(self):  return "#C1440E"
    def symbol(self): return "W"

    def _act(self, eco):
        nbrs = eco.grid.neighbors(self.x, self.y)
        prey_cells  = [c for c in nbrs if isinstance(eco.grid.animal_at(*c), Sheep)]
        empty_cells = [c for c in nbrs if eco.grid.animal_at(*c) is None]

        if prey_cells:
            nx, ny = random.choice(prey_cells)
            prey = eco.grid.animal_at(nx, ny)
            prey.alive = False
            eco.grid.remove_animal(prey)           # remove immediately so grid stays consistent
            eco.grid.move_animal(self, nx, ny)
            self.energy += self.sheep_energy
        elif empty_cells:
            nx, ny = random.choice(empty_cells)
            eco.grid.move_animal(self, nx, ny)

        if self.energy >= self.repr_threshold:
            self.energy //= 2
            spawn = [c for c in eco.grid.neighbors(self.x, self.y)
                     if eco.grid.animal_at(*c) is None]
            if spawn:
                bx, by = random.choice(spawn)
                return Wolf(bx, by, self.energy, self.repr_threshold, self.sheep_energy)
        return None
