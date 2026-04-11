"""Grid: two-layer spatial container used by Ecosystem via composition."""


class Grid:
    """owns the grass layer and animal layer for the simulation space."""

    def __init__(self, width, height):
        self.width  = width
        self.height = height
        self._grass   = [[False] * width for _ in range(height)]
        self._animals = [[None]  * width for _ in range(height)]

    def neighbors(self, x, y):
        """moore neighbourhood with toroidal (wrap-around) edges."""
        return [
            ((x + dx) % self.width, (y + dy) % self.height)
            for dx in (-1, 0, 1) for dy in (-1, 0, 1)
            if (dx, dy) != (0, 0)
        ]

    # ── grass ──────────────────────────────────────────────────────────────────

    def has_grass(self, x, y):    return self._grass[y][x]
    def place_grass(self, x, y):  self._grass[y][x] = True
    def remove_grass(self, x, y): self._grass[y][x] = False

    def grass_count(self):
        return sum(self._grass[y][x] for y in range(self.height) for x in range(self.width))

    # ── animals ────────────────────────────────────────────────────────────────

    def animal_at(self, x, y):
        return self._animals[y][x]

    def place_animal(self, a):
        self._animals[a.y][a.x] = a

    def remove_animal(self, a):
        if self._animals[a.y][a.x] is a:
            self._animals[a.y][a.x] = None

    def move_animal(self, a, nx, ny):
        self.remove_animal(a)
        a.x, a.y = nx, ny
        self._animals[ny][nx] = a

    # ── iteration ──────────────────────────────────────────────────────────────

    def iter_cells(self):
        """yield (x, y, has_grass, animal) for every cell."""
        for y in range(self.height):
            for x in range(self.width):
                yield x, y, self._grass[y][x], self._animals[y][x]
