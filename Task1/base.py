"""abstract base classes: Entity -> Organism -> Animal."""

from abc import ABC, abstractmethod


class Entity(ABC):
    """abstract base: anything that occupies a grid position."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @abstractmethod
    def color(self): 
        ...

    @abstractmethod
    def symbol(self): 
        ...


class Organism(Entity):
    """entity with energy and an alive/dead lifecycle."""

    def __init__(self, x, y, energy):
        super().__init__(x, y)
        self.energy = energy
        self.alive  = True

    @abstractmethod
    def update(self, eco): 
        ...


class Animal(Organism):
    """mobile organism with reproduction; subclasses implement _act."""

    def __init__(self, x, y, energy, repr_threshold):
        super().__init__(x, y, energy)
        self.repr_threshold = repr_threshold

    @abstractmethod
    def _act(self, eco):
        """one step of behaviour; returns offspring or None."""

    def update(self, eco):
        self.energy -= 1
        if self.energy <= 0:
            self.alive = False
            return None
        return self._act(eco)
