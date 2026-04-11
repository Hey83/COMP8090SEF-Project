"""Ecosystem: simulation engine that composes a Grid and drives organism lifecycles."""

import random
from grid import Grid
from organisms import Sheep, Wolf


class Ecosystem:
    """owns a Grid (composition) and orchestrates all simulation rules."""

    def __init__(self, cfg):
        self.cfg        = cfg
        random.seed(cfg["seed"])
        self.grid       = Grid(cfg["grid_w"], cfg["grid_h"])   # composition
        self.animals    = []
        self.step_count = 0
        self._seed()

    def _seed(self):
        cells = [(x, y) for y in range(self.grid.height) for x in range(self.grid.width)]
        random.shuffle(cells)

        grass_n = int(len(cells) * self.cfg["grass_pct"] / 100)
        for x, y in cells[:grass_n]:
            self.grid.place_grass(x, y)

        # shared iterator so sheep and wolves never start on the same cell
        pool = iter(cells)

        def place(cls, n, **kw):
            if n <= 0:
                return
            placed = 0
            for x, y in pool:
                if self.grid.animal_at(x, y) is None:
                    a = cls(x, y, **kw)
                    self.grid.place_animal(a)
                    self.animals.append(a)
                    placed += 1
                    if placed >= n:
                        break

        place(Sheep, self.cfg["n_sheep"],
              energy=self.cfg["sheep_energy"], repr_threshold=self.cfg["sheep_repr"],
              grass_energy=self.cfg["grass_energy"])
        place(Wolf, self.cfg["n_wolves"],
              energy=self.cfg["wolf_energy"], repr_threshold=self.cfg["wolf_repr"],
              sheep_energy=self.cfg["sheep_energy_val"])

    def step(self):
        random.shuffle(self.animals)   # randomise order to avoid spatial bias
        offspring = []

        for animal in self.animals:
            if animal.alive:
                child = animal.update(self)
                if child:
                    offspring.append(child)

        for a in self.animals:
            if not a.alive:
                self.grid.remove_animal(a)
        self.animals = [a for a in self.animals if a.alive]

        for child in offspring:
            if self.grid.animal_at(child.x, child.y) is None:
                self.grid.place_animal(child)
                self.animals.append(child)

        # stochastic grass regrowth
        rate = self.cfg["grass_rate"]
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                if not self.grid.has_grass(x, y) and random.random() < rate:
                    self.grid.place_grass(x, y)

        self.step_count += 1

    def counts(self):
        sheep = wolves = 0
        for a in self.animals:
            if isinstance(a, Sheep): sheep  += 1
            else:                    wolves += 1
        return self.grid.grass_count(), sheep, wolves
